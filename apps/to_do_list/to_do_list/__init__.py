while True:
    user_action = input("Type add, show, edit, complete or exit: ")
    user_action = user_action.strip()

    match user_action:
        case "add":
            user_input = input("Enter an item to your list: ") + "\n"

            file = open("to_do_list.txt", "r")
            to_do_list = file.readlines()
            file.close()

            to_do_list.append(user_input)

            file = open("to_do_list.txt", "w")
            file.writelines(to_do_list)
            file.close()

        case "show":
            file = open("to_do_list.txt", "r")
            to_do_list = file.readlines()
            file.close()

            for index, item in enumerate(to_do_list):
                row = f"{index + 1}- {item}"
                print(row)
        case "edit":
            number = int(
                input(
                    "Which item within the list would you like to edit? Select a number.: "
                )
            )
            number = number - 1
            updated_list = input("Please enter the new item: ")
            to_do_list[number] = updated_list
        case "exit":
            break
        case "complete":
            number = int(input("Number of the todo to complete: "))
            to_do_list.pop(number - 1)
        case _:
            print("Please enter an available option: ")

print("Thank you for using our application.")
