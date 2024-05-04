from datetime import datetime


class Transaction:
    def __init__(self, date, category, amount, description):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description


class PersonalFinanceApp:
    def __init__(self, filename):
        self.filename = filename
        self.transactions = []
        self.load_data()

    def load_data(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            for i in range(0, len(lines), 5):
                date = datetime.strptime(lines[i].strip().split(": ")[1], "%Y-%m-%d")
                category = lines[i + 1].strip().split(": ")[1]
                amount = int(lines[i + 2].strip().split(": ")[1])
                description = lines[i + 3].strip().split(": ")[1]
                self.transactions.append(Transaction(date, category, amount, description))

    def save_data(self):
        with open(self.filename, 'w') as file:
            for transaction in self.transactions:
                file.write(f"Дата: {transaction.date.strftime('%Y-%m-%d')}\n")
                file.write(f"Категория: {transaction.category}\n")
                file.write(f"Сумма: {transaction.amount}\n")
                file.write(f"Описание: {transaction.description}\n\n")

    def display_balance(self):
        total_income = sum(transaction.amount for transaction in self.transactions if transaction.category == 'Доход')
        total_expense = sum(transaction.amount for transaction in self.transactions if transaction.category == 'Расход')
        total_balance = total_income - total_expense
        print("Текущий баланс:")
        print(f"Доходы: {total_income} руб.")
        print(f"Расходы: {total_expense} руб.")
        print(f"Баланс: {total_balance} руб.")

    def add_transaction(self, date, category, amount, description):
        self.transactions.append(Transaction(date, category, amount, description))
        self.save_data()
        print("Запись успешно добавлена.")

    def edit_transaction(self, index, date, category, amount, description):
        self.transactions[index] = Transaction(date, category, amount, description)
        self.save_data()
        print("Запись успешно отредактирована.")

    def search_transactions(self, category=None, date=None, amount=None):
        results = []
        for transaction in self.transactions:
            if (not category or transaction.category == category) and \
               (not date or transaction.date == date) and \
               (not amount or transaction.amount == amount):
                results.append(transaction)
        return results


def main():
    app = PersonalFinanceApp("scratch.txt")
    while True:
        print("\nВыберите действие:")
        print("1. Вывод баланса")
        print("2. Добавление записи")
        print("3. Редактирование записи")
        print("4. Поиск по записям")
        print("5. Выход")
        choice = input("Ваш выбор: ")

        if choice == '1':
            app.display_balance()
        elif choice == '2':
            try:
                date = datetime.strptime(input("Введите дату (ГГГГ-ММ-ДД): "), "%Y-%m-%d")
                category = input("Введите категорию (Доход/Расход): ")
                amount = int(input("Введите сумму: "))
                description = input("Введите описание: ")
                app.add_transaction(date, category, amount, description)

            except ValueError as error:
                print("Неправильно указана дата. Ошибка {}".format(error))
                main()
        elif choice == '3':
            try:
                index = int(input("Введите индекс записи для редактирования: "))
                date = datetime.strptime(input("Введите новую дату (ГГГГ-ММ-ДД): "), "%Y-%m-%d")
                category = input("Введите новую категорию (Доход/Расход): ")
                amount = int(input("Введите новую сумму: "))
                description = input("Введите новое описание: ")
                app.edit_transaction(index, date, category, amount, description)
            except ValueError as error:
                print("Произошла ошибка: {}".format(error))
                main()
        elif choice == '4':
            category = input("Введите категорию (Доход/Расход) или нажмите Enter для пропуска: ")
            date_str = input("Введите дату (ГГГГ-ММ-ДД) или нажмите Enter для пропуска: ")
            date = datetime.strptime(date_str, "%Y-%m-%d") if date_str else None
            amount = int(input("Введите сумму или нажмите Enter для пропуска: ")) if input else None
            results = app.search_transactions(category, date, amount)
            if results:
                print("Результаты поиска:")
                for result in results:
                    print(f"Дата: {result.date.strftime('%Y-%m-%d')}, Категория: {result.category}, Сумма: {result.amount}, Описание: {result.description}")
            else:
                print("Ничего не найдено.")
        elif choice == '5':
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите существующий вариант.")


if __name__ == "__main__":
    main()
