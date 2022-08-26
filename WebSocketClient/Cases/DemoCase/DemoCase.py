from Core.BaseCase import BaseCase

class DemoCase(BaseCase):
    def run(self):
        body = {'type':['Shop1'],'opt':0}
        self.add_check('check_1','game.RequestGetShopInfo',body)
        self.client.run_forever()
        send = self.get_send('check_1')
        res = self.get_res('check_1')
        shoptype = res['infoes'][0]['type']
        self.do_assert('Shop1',shoptype,'check_1')