import itertools

class CostClient(object):
    CURRENT_COST_URL = '/olap_reports/cost/current'
    HISTORY_COST_URL = '/olap_reports/cost/history'
    ACCOUNTS_HISTORY_COST_URL = '/olap_reports/custom/893353198679'

    def __init__(self, client):
        self.client = client

    def list_months(self, type):
        response = self.client.get(self.ACCOUNTS_HISTORY_COST_URL)

        list_of_months = []
        months = response['dimensions'][0]["time"]

        for month in months:
            label = month['label']
            list_of_months.append(label.encode('ascii'))

        return list_of_months

    def list_accounts(self, account_type):
        response = self.client.get(self.CURRENT_COST_URL)

        list_of_accounts = []
        accounts_list = response['dimensions'][0][account_type]

        for account in accounts_list:
            label = account['label']
            list_of_accounts.append(label.encode('ascii'))

        return list_of_accounts

    def list_service(self):
        response = self.client.get(self.HISTORY_COST_URL)

        list_of_services = []
        service_list = response['dimensions'][1]['AWS-Service-Category']

        for service in service_list:
            label = service['label']
            list_of_services.append(label.encode('ascii'))


        return list_of_services


    def get_current(self, account_type='AWS-Account', account_name=None):
        response = self.client.get(self.CURRENT_COST_URL)

        accounts_total_cost = []

        list_of_aws_accounts = self.list_accounts(account_type)

        cost_response = response['data']
        for accounts_total in cost_response:
            accounts_total_cost.append(accounts_total[0][0])

        cost_by_account = dict(zip(list_of_aws_accounts, accounts_total_cost))

        return cost_by_account

    def account_history(self,
                         account_type='AWS-Account'):
        response = self.client.get(self.ACCOUNTS_HISTORY_COST_URL)

        list_of_months = self.list_months(self.HISTORY_COST_URL)
        list_of_accounts = self.list_accounts(account_type)

        accounts_history = {}

        cost_response = response['data']
        for month_cost, each_month in zip(cost_response, list_of_months):
            accounts_cost_history_by_month = dict(zip(list_of_accounts, sum(month_cost, [])))
            months_total = {each_month: accounts_cost_history_by_month}
            for key, value in months_total.iteritems():
                accounts_history[key] = value

        return accounts_history

    def service_history(self,
                            account_type,
                            service,
                            month=None):
        response = self.client.get(self.HISTORY_COST_URL)

        list_of_months = self.list_months(self.HISTORY_COST_URL)

        service_cost_by_month = []
        fetch_services = self.list_service()

        cost_response = response['data']

        for called_service in cost_response:
            service_cost_history_by_month = dict(zip(fetch_services, called_service))
            service_cost_by_month.append(service_cost_history_by_month[service][0])


        cost_history_for_service = dict(zip(list_of_months,
                                            service_cost_by_month))
        return cost_history_for_service

    def services_history(self,
                        account_type,
                        service,
                        month=None):
        response = self.client.get(self.HISTORY_COST_URL)

        list_of_months = self.list_months(self.HISTORY_COST_URL)
        asked_month = list_of_months.index(month)

        fetch_services = self.list_service()

        cost_response = response['data']
        cost_of_month = list(itertools.chain(*cost_response[asked_month]))

        service_cost_history_by_month = dict(zip(fetch_services, cost_of_month))

        return service_cost_history_by_month