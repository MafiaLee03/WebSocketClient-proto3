from Core.BaseCase import BaseCase

class OtherCase(BaseCase):
    def run(self):
        body = {'item_id':2032,'item_count':1001}
        self.add_check('check_1','game.RequestUseItem',body)
        self.client.run_forever()
        send = self.get_send('check_1')
        res = self.get_res('check_1')
        error_code = res['code']
        self.do_assert('ITEM_NOTENOUGH',error_code,'check_1')