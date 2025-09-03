def user_interaction():
    while True:
        action = yield "What would you like to do?"
        if action == "quit":
            print("goodbye")
            break
        elif action == "greet":
            print("Hello bro")
        else:
            print("Unknown action: {action}")


interaction = user_interaction() # Generator
print(next(interaction)) # Start the generator
print(interaction.send("greet"))
print(interaction.send("dog"))
print(interaction.send("quit"))

