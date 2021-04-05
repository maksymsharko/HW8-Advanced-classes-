from __future__ import annotations
from abc import ABC, abstractmethod
import random
import uuid
import time
from typing import Dict, Any


class Animal(ABC):
    def __init__(self, strength: int, speed: int):
        self.id = None
        self.max_strength = strength
        self.current_strength = strength
        self.speed = speed

    @abstractmethod
    def eat(self, forest: Forest):
        raise NotImplementedError('Your method is not implemented')


class Predator(Animal):
    def eat(self, forest: Forest):
        prey = random.choice(list(forest.animals.values()))
        if prey.id == self.id:
            print("No prey. The predator did hot catch anyone")
        else:
            print(f"The {__class__.__name__} has {self.current_strength} strength and has {self.speed} speed hunts for "
                  f"the {prey.__class__.__name__} that has {prey.current_strength} strength and {prey.speed} speed")
            if self.speed > prey.speed:
                print("The predator caught the prey")
                if self.current_strength > prey.current_strength:
                    print("The predator caught up with the prey")
                    catching(prey)
                    strength_recovery(self)

                else:
                    print("The predator did not catch up with the prey")
                    uncatching(self)
                    uncatching(prey)

            else:
                print("The prey escaped")
                unsuccessful_pursuit(self)
                unsuccessful_pursuit(prey)


class Herbivorous(Animal):
    def eat(self, forest: Forest):
        strength_recovery(self)


def strength_recovery(animal: AnyAnimal):
    print(f"The {animal.__class__.__name__} is eating with {animal.current_strength} strength")
    if animal.current_strength + animal.max_strength * 0.5 >= animal.max_strength:
        animal.current_strength = animal.max_strength
    else:
        animal.current_strength = round(animal.current_strength + animal.max_strength * 0.5)
    print(f"The {animal.__class__.__name__} ate and was able to regain his strength to {animal.current_strength}")


def catching(herbivorous: AnyAnimal):
    forest.remove_animal(herbivorous)
    print(f"The {herbivorous.__class__.__name__} could not escape")


def uncatching(animal: AnyAnimal):
    if animal.current_strength - animal.max_strength * 0.3 <= 0:
        forest.remove_animal(animal)
        print(f"The {animal.__class__.__name__} died")
    else:
        animal.current_strength = round(animal.current_strength - animal.max_strength * 0.3)
        print(f"The {animal.__class__.__name__} could not escape with {animal.current_strength} strength")


def unsuccessful_pursuit(animal: AnyAnimal):
    if animal.current_strength - animal.max_strength * 0.3 <= 0:
        forest.remove_animal(animal)
        print(f"The {animal.__class__.__name__} died")
    else:
        animal.current_strength = round(animal.current_strength - animal.max_strength * 0.3)
        print(f"The {animal.__class__.__name__} has {animal.current_strength} strength remained after a failed chase")


AnyAnimal: Any[Herbivorous, Predator]


class Forest:

    def __init__(self):
        self.animals: Dict[str, AnyAnimal] = dict()

    def add_animal(self, animal: AnyAnimal):
        print(f"This animal was added to the Forest", animal)
        self.animals.update({animal.id: animal})

    def remove_animal(self, animal: AnyAnimal):
        print(f"The {animal.__class__.__name__} removed from the forest")
        self.animals.pop(animal.id)

    def remaining_predator(self):
        global predator
        for predator in list(self.animals.values()):
            if predator.__class__.__name__ == "Predator":
                print(f"The {predator.__class__.__name__} is in the Forest")
                return True
        print(f"The {predator.__class__.__name__} resides in the Forest")
        return False

    def __iter__(self):
        self.arr = 0
        self.animal_point = list(self.animals.values())
        return self

    def __next__(self):
        self.arr = self.arr + 1
        if self.arr <= len(self.animal_point):
            return self.animal_point[self.arr - 1]
        else:
            raise StopIteration


def animal_generator():
    while True:
        generator = random.choice((Herbivorous(random.randrange(25, 100, 1), random.randrange(25, 100, 1)),
                                   Predator(random.randrange(25, 100, 1), random.randrange(25, 100, 1))))
        generator.id = uuid.uuid4()
        yield generator


if __name__ == "__main__":
    forest = Forest()
    nature = animal_generator()
    for x in range(10):
        animal = next(nature)
        print(animal.__dict__)
        forest.add_animal(animal)
    print([{predator.__class__.__name__: predator.__dict__} for predator in list(forest.animals.values())])
    while True:
        if not forest.remaining_predator():
            break
        random.choice(list(forest.animals.values())).eat(forest)
        time.sleep(1)
    print("So, Game over!")
