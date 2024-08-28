from ui.roadmap import Roadmap

singleton = Roadmap()
new_singleton = Roadmap()
 
print(singleton is new_singleton)