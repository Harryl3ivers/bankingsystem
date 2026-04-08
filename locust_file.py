# from locust import HttpUser, task, between
# import random

# class BankUser(HttpUser):
#     wait_time = between(1, 2)

#     def on_start(self):
#         self.account_number = f"ACC{random.randint(1000,9999)}"

#         self.client.post("/accounts/", params={
#             "account_number": self.account_number,
#             "account_name": "Test User",
#             "balance": 100
#         })

#     @task
#     def deposit(self):
#         self.client.post("/deposit/", params={
#             "account_number": self.account_number,
#             "amount": random.randint(1, 20)
#         })

#     @task
#     def withdraw(self):
#         self.client.post("/withdraw/", params={
#             "account_number": self.account_number,
#             "amount": random.randint(1, 10)
#         })