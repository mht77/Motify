from locust import HttpUser, task, between

token = ''


class UserInfo(HttpUser):
    wait_time = between(1, 2.5)

    weight = 1

    @task
    def user_account(self):
        self.client.get('/api/account/')

    def on_start(self):
        self.client.headers = {'Authorization': 'Bearer ' + token}


class Artists(HttpUser):
    wait_time = between(1, 2.5)

    weight = 2

    def on_start(self):
        self.client.headers = {'Authorization': 'Bearer ' + token}

    @task
    def artists(self):
        self.client.get('/api/artists/')


class UserPlayer(HttpUser):
    wait_time = between(0, 1)

    weight = 3

    def on_start(self):
        self.client.headers = {'Authorization': 'Bearer ' + token}

    @task
    def player_token(self):
        self.client.get('/api/user_player/')
