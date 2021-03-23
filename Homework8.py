from __future__ import annotations
import time
from abc import ABC, abstractmethod
import uuid
import random
from typing import Any, Dict



class Animal(ABC):
    def __init__(self, strength: int, speed: int ):
        self.id = None
        self.max_strength = strength
        self.current_strength = strength
        self.speed = speed

    @abstractmethod
    def eat(self, forest: Forest):
        raise NotImplementedError("Method is not implemented")



class Predator(Animal):

    def eat(self, forest: Forest):
        result = random.choice(list(forest.animals.values()))
        if result.id == self.id:
            print("No herbivorous in the forest")
        else:
            if (self.speed > result.speed) and (self.current_strength > result.current_strength):
                print("Prey eating")
                curr = self.current_strength
                self.current_strength = min(self.current_strength + self.max_strength * 0.5, self.max_strength)
                print(f'The predator has recovered {self.current_strength - curr} strength')
                forest.animals[result.id].current_strength = 0
            else:
                self.current_strength = self.current_strength - self.max_strength * 0.3
                print('The predator failed to catch prey. Strength are lost')
                forest.animals[result.id].current_strength = forest.animals[result.id].current_strength - 0.3 * \
                                                             forest.animals[result.id].max_strength

    def __str__(self):
        return f'{self.__class__.__name__}'


class Herbivorous(Animal):

    def eat(self, forest: Forest):
        print('Herbivorous is eating')
        curr = self.current_strength
        self.current_strength = min(self.current_strength + self.max_strength * 0.5, self.max_strength)
        print(f'Herbivorous has recovered {self.current_strength - curr} strength')

    def __str__(self):
        return f'{self.__class__.__name__}'



AnyAnimal: Any[Herbivorous, Predator]

class Forest:

    def __init__(self):
        self.animals: Dict[str, AnyAnimal] = dict()

    def add_animal(self, animal: AnyAnimal):
        print(f'A {animal} is added', animal)
        self.animals.update({animal.id: animal})

    def remove_animal(self, animal: AnyAnimal):
        print(f'{animal, id} is removed from forest')
        self.animals.pop(animal.id)

    def any_predator_left(self):
        return not all(isinstance(animal, Herbivorous) for animal in self.animals.values())

    def __iter__(self):
        self.num = 0
        self.value = list(self.animals.values())

    def __next__(self):
        self.num += 1
        if self.num <= len(self.value):
            return self.value[self.num - 1]
        else:
            raise StopIteration


def animal_generator():
    while True:
        generator = random.choice((Herbivorous(random.randint(25, 100), random.randint(25, 100)),
                                  Predator(random.randint(25, 100), random.randint(25, 100))))
        generator.id = uuid.uuid4()
        yield generator

if __name__ == "__main__":
    nature = animal_generator()
    forest = Forest()

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







