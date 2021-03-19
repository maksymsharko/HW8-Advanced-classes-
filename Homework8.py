from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict
import time
import uuid
import random

@abstractmethod
class Animal(ABC):

    def __init__(self, strength: int, speed: int ):
        self.id = None
        self.max_strength = strength
        self.current_strength = strength
        self.speed = speed

    def eat(self, forest: Forest):
        pass



class Predator(Animal):
    def __init__(self,  strength: int, speed: int):
        super(Predator, self).__init__(strength, speed)
        self.id = None
        self.max_strength = strength
        self.current_strength = strength
        self.speed = speed

    def eat(self, forest: Forest):
        result = random.choice(list(forest.animals.values()))
        if result.id == self.id:
            print("No herbivorous in the forest")
        else:
            if (self.speed > result.speed) and (self.current_strength > result.current_strength):
                print("Prey from a predator")
                curr = self.current_strength
                self.current_strength = min(self.current_strength + self.max_strength * 0.5, self.max_strength)
                print(f'The predator has recovered {self.current_strength} strength')
            else:
                self.current_strength = self.current_strength - self.max_strength * 0.3
                print('The predator failed to catch prey. Strength are lost')
                forest.animals[result.id].current_strength = forest.animals[result.id].current_strength - 0.3 * \
                                                          forest.animals[result.id].max_strength



class Herbivorous(Animal):

    def __init__(self, strength: int, speed: int):
        super(Herbivorous, self).__init__(strength, speed)
        self.id = None
        self.max_strength = strength
        self.current_strength = strength
        self.speed = speed


    def eat(self, forest: Forest):
        print('Herbivorous is eating')
        curr = self.current_strength
        self.current_strength = min(self.current_strength + self.max_strength * 0.5, self.max_strength)
        print(f'Herbivorous has recovered {self.current_strength - curr} strength')



AnyAnimal: Any[Herbivorous, Predator]

class Forest():

    def __init__(self):
        self.animals: Dict[str, AnyAnimal] = dict()

    def add_animal(self, animal: AnyAnimal):
        print(f'A {animal} is added', animal)
        self.animals.update({animal.id: animal})

    def remove_animal(self, animal: AnyAnimal):
        print(f'{animal, id} is removed')
        self.animals.pop(animal.id)

    def any_predator_left(self):
        return not all(isinstance(animal, Herbivorous) for animal in self.animals.values())

def animal_generator():
    while True:
        generator = random.choice((Herbivorous(random.randint(25, 100), random.randint(25, 100)),
                                  Predator(random.randint(25, 100), random.randint(25, 100))))
        generator.id = uuid.uuid4()
        yield generator

if __name__ == "__main__":
    forest = Forest()
    nature = animal_generator()


    for i in range(10):
        animal = next(nature)
        forest.add_animal(animal)

    while True:
        animal_to_remove = []
        for animal in forest.animals.values():
            if animal.current_strength < 1:
                animal_to_remove.append(animal.id)
        for animal_id in animal_to_remove:
            forest.remove_animal(forest.animals[animal_id])
        if not forest.any_predator_left():
            print('Predators are dead. No predators in the forest')
            break
        for animal in forest.animals.values():
            animal.eat(forest=forest)
        time.sleep(1)







