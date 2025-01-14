from llabot import LLaBot, UserData

if __name__ == "__main__":
  llabot = LLaBot()
  user_data = UserData.from_json_file()
  llabot.add_bot()
  llabot.start_chat(0, user_data)
  while True:
    user_input = input("Enter a message ('exit' to quit): ")
    if user_input.lower() == "exit":
      break
    print(llabot.generate_response(0, user_input))