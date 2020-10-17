import vk
from time import sleep, time



class VKParser:
    def __init__(self):
        self.token = '4d68247a4d68247a4d68247a9d4d1be5bf44d684d68247a1239389d4bbd08c2e6085e43'
        self.users = []
        self.friendship = []
        self.vk_api = vk.API(vk.Session(access_token=self.token))
        self.users_count = 0
    def get_group_users(self, groupid): # First runable method
        try:
            api_ans = self.vk_api.groups.getMembers(group_id=groupid, fields = ('is_private','photo_100'), v=5.124)
            self.users = api_ans.get('items')
            self.users_count = api_ans.get('count')
        except:
            print('Ошибка API: группа запретила доступ к ее подписчикам')
            exit()
    def get_users(self):
        return self.users
    def get_friendship(self):
        return self.friendship
    def __get_friends__(self, id):
        return self.vk_api.friends.get(user_id=id,fields = ('is_private','photo_100'), v=5.124).get('items')
        sleep(.10)
    def is_in(self, id):
        for i in self.users:
            if id == i.get('id'):
                return True
        return False
    def complete_friendship(self): # Вызывается с заполненным списком друзей (т.е. после get_group_users)
        end_users = [] # объявляем новый  временный массив во избежание потери данных при изменении self.users
        index_id = []
        average_exe_time = []
        counter = 0
        for i in self.users:
            cur_time = time()
            k = i.get('id')
            has_friend = False
            if i.get('is_closed')==False:
                for j in self.__get_friends__(k): # перебираем друзей человека под id i 
                    p = j.get('id')
                    if self.is_in(p) and j.get('is_closed')==False: # если переб-ый друг есть в списке под-ков группы
                        #и такой записи ранее не было во friendship: добавляем запись в  friendship
                        if (p,k) not in self.friendship:
                            self.friendship.append((k,p))
                            if p not in index_id:
                                end_users.append(j)
                                index_id.append(p)
                        has_friend = True
            if has_friend and k not in index_id:
                end_users.append(i)
                index_id.append(k)
            if len(average_exe_time)<10:
                average_exe_time.append(cur_time - time())
                if counter %10 == 0:
                    print('Расчет оставшегося времени...')
            else:
                if counter %20 == 0:
                    print('Обработано {} из {} подписчиков. Примерное время ожидания: {} секунд.'.format(str(counter),str(self.users_count), str(sum(average_exe_time)/len(average_exe_time) * (counter - self.users_count))  ))
            #sleep(.20)
            counter+=1
        self.users = end_users 


