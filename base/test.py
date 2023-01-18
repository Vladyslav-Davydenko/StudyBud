from dataclasses import dataclass

@dataclass
class Greetings():
    greeting: str
    audience: str

    def __str__(self) -> str:
        return f"{self.greeting} {self.audience} !"


def main():
    g = Greetings("Hello", "World")
    print(g)

if __name__ == "__main__":
    main()