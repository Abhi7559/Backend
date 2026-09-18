def distance_converter():
    print("Distance Converter")
    print("1. Kilometers to Miles")
    print("2. Miles to Kilometers")

    choice = input("Choose conversion: ")

    if choice == "1":
        try:
            value = float(input("Enter kilometers: "))
            converted = value * 0.621371
            print(f"Result: {value:.2f} km = {converted:.2f} miles")
        except ValueError:
            print("Please enter a valid number.")

    elif choice == "2":
        try:
            value = float(input("Enter miles: "))
            converted = value * 1.60934
            print(f"Result: {value:.2f} miles = {converted:.2f} km")
        except ValueError:
            print("Please enter a valid number.")

    else:
        print("Please choose 1 or 2.")


def temperature_converter():
    print("Temperature Converter")
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")

    choice = input("Choose conversion: ")

    if choice == "1":
        try:
            value = float(input("Enter Celsius: "))
            converted = (value * 9 / 5) + 32
            print(f"Result: {value:.2f} °C = {converted:.2f} °F")
        except ValueError:
            print("Please enter a valid number.")

    elif choice == "2":
        try:
            value = float(input("Enter Fahrenheit: "))
            converted = (value - 32) * 5 / 9
            print(f"Result: {value:.2f} °F = {converted:.2f} °C")
        except ValueError:
            print("Please enter a valid number.")

    else:
        print("Please choose 1 or 2.")


def weight_converter():
    print("Weight Converter")
    print("1. Kilograms to Pounds")
    print("2. Pounds to Kilograms")

    choice = input("Choose conversion: ")

    if choice == "1":
        try:
            value = float(input("Enter kilograms: "))
            converted = value * 2.20462
            print(f"Result: {value:.2f} kg = {converted:.2f} lb")
        except ValueError:
            print("Please enter a valid number.")

    elif choice == "2":
        try:
            value = float(input("Enter pounds: "))
            converted = value * 0.453592
            print(f"Result: {value:.2f} lb = {converted:.2f} kg")
        except ValueError:
            print("Please enter a valid number.")

    else:
        print("Please choose 1 or 2.")


def main():
    while True:
        print("Measurement Converter")
        print("1. Distance")
        print("2. Temperature")
        print("3. Weight")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            distance_converter()

        elif choice == "2":
            temperature_converter()

        elif choice == "3":
            weight_converter()

        elif choice == "4":
            print("Thank you for using Measurement Converter.")
            break

        else:
            print("Please choose an option from 1 to 4.")


if __name__ == "__main__":
    main()