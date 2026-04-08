# -------------------------------
# Response Class
# -------------------------------
class Response:
    def __init__(self, keyword="", response=""):
        self.keyword = keyword
        self.response = response

    def get_keyword(self):
        return self.keyword

    def get_response(self):
        return self.response

    def set_keyword(self, keyword):
        self.keyword = keyword

    def set_response(self, response):
        self.response = response


# -------------------------------
# Base Class: Chatbot
# -------------------------------
class Chatbot:
    max_size = 100  # Maximum number of keyword-response pairs

    def __init__(self, bot_name, file_name):
        self.name = bot_name
        self.filename = file_name
        self.responses = []
        self.current_size = 0
        self.load_responses()

    # Helper method to convert string to lowercase
    def to_lower_case(self, text):
        return text.lower()

    # Polymorphism: Base greet method
    def greet(self):
        print(f"Hi! I'm {self.name}. How can I help you today?")

    def farewell(self):
        print("Goodbye! Have a great day!")

    def respond(self, user_input):
        lower_input = self.to_lower_case(user_input)
        found = False

        for response_obj in self.responses:
            if response_obj.get_keyword() in lower_input:
                print(response_obj.get_response())
                found = True
                break

        if not found:
            print("I don't understand. Can you teach me a response for this?")
            keyword = input("Enter a keyword or phrase: ")
            response = input("Enter the response for this keyword or phrase: ")
            self.learn(keyword, response)

    def learn(self, keyword, response):
        if self.current_size < self.max_size:
            new_response = Response(self.to_lower_case(keyword), response)
            self.responses.append(new_response)
            self.current_size += 1
            self.save_response_to_file(keyword, response)
            print("I've learned a new response!")
        else:
            print("Sorry, I can't learn any more responses. My memory is full.")

    def load_responses(self):
        try:
            with open(self.filename, "r") as infile:
                lines = infile.readlines()

                self.responses = []
                self.current_size = 0

                for i in range(0, len(lines), 2):
                    if i + 1 < len(lines) and self.current_size < self.max_size:
                        keyword = lines[i].strip()
                        response = lines[i + 1].strip()

                        new_response = Response(self.to_lower_case(keyword), response)
                        self.responses.append(new_response)
                        self.current_size += 1
        except FileNotFoundError:
            print("Unable to open the file.")

    def save_response_to_file(self, keyword, response):
        try:
            with open(self.filename, "a") as outfile:
                outfile.write(keyword + "\n")
                outfile.write(response + "\n")
        except:
            print("Unable to open the file.")


# -------------------------------
# Derived Class: AutoMaintenanceChatbot
# -------------------------------
class AutoMaintenanceChatbot(Chatbot):
    def __init__(self, bot_name, file_name):
        super().__init__(bot_name, file_name)

    def custom_service_info(self):
        print("We provide a range of auto maintenance services. For more details, please ask about specific services.")

    # Polymorphism: Overriding greet method
    def greet(self):
        print(f"Hello! Welcome to the Auto Maintenance Workshop. I'm {self.name}. How can I assist you today?")


# -------------------------------
# Separate Class: EmergencyService
# -------------------------------
class EmergencyService:
    def provide_emergency_info(self):
        print("In case of roadside emergencies, please contact +92 316 5119292 for immediate assistance.")


# -------------------------------
# Another Derived Class: WorkshopChatbot
# -------------------------------
class WorkshopChatbot(AutoMaintenanceChatbot):
    def __init__(self, bot_name, file_name):
        super().__init__(bot_name, file_name)
        self.emergency_service = EmergencyService()  # Composition

    def provide_emergency_service(self):
        self.emergency_service.provide_emergency_info()


# -------------------------------
# Main Function
# -------------------------------
def main():
    my_bot = WorkshopChatbot("MJ's Bot", "MJ-details.txt")

    my_bot.greet()

    while True:
        user_input = input("You: ")

        if my_bot.to_lower_case(user_input) == "bye" or my_bot.to_lower_case(user_input) == "exit":
            my_bot.farewell()
            break
        elif my_bot.to_lower_case(user_input) == "emergency":
            my_bot.provide_emergency_service()
        else:
            my_bot.respond(user_input)


# -------------------------------
# Program Entry Point
# -------------------------------
if __name__ == "__main__":
    main()