import time
import random
import os
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
# Подключение к Ethereum (замени на свой RPC)
INFURA_URL = "https://1rpc.io/eth"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Данные аккаунта
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ADDRESS = Web3.to_checksum_address("0xA6851E37665927D061EeFF377d144d638884dd9f")

# Проверка соединения
assert web3.is_connected(), "Не удалось подключиться к Ethereum"

def send_transaction():
    while True:  # Цикл, чтобы автоматически исправлять ошибку
        try:

            nonce = web3.eth.get_transaction_count(ADDRESS, "pending")  # Берём актуальный nonce


            base_fee = web3.eth.fee_history(1, "latest")["baseFeePerGas"][0]
            max_priority_fee = web3.to_wei(0.1, "gwei")
            max_fee = base_fee + max_priority_fee

            z = random.randint(100, 999)
            ADDRESS01 = Web3.to_checksum_address(f"0xA6851E37665927D061EeFF377d144d638014d{z}")

            tx = {
                "to": ADDRESS01,
                "value": web3.to_wei(0.0, "ether"),
                "nonce": nonce,
                "gas": 21_000,
                "maxFeePerGas": max_fee,
                "maxPriorityFeePerGas": max_priority_fee,
                "chainId": web3.eth.chain_id,
            }

            signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            print(f"Отправлена транзакция: {tx_hash.hex()} за {web3.from_wei(21_000 * max_fee, 'ether')} ETH")
            break  # Если транзакция отправлена успешно, выходим из цикла

        except web3.exceptions.Web3RPCError as e:
            if "nonce too low" in str(e):
                print("Nonce слишком низкий, обновляем...")
                time.sleep(3)  # Ждём 3 секунды и пробуем снова
            else:
                raise  # Если ошибка другая, пробрасываем её
# Отправляем 100 транзакций с задержками
for i in range(100):
    send_transaction()
    delay = random.randint(18, 33)
    print(f"Задержка перед следующей транзакцией: {delay} секунд")
    time.sleep(delay)

print("Все 100 транзакций отправлены!")
