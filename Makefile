CXX = g++
CXXFLAGS = -std=c++2a -Wall -c
LXXFLAGS = -std=c++2a
OBJECTS = main.o 
TARGET = main


$(TARGET): $(OBJECTS)
	$(CXX) $(LXXFLAGS) $(OBJECTS) -o $(TARGET)
main.o: main.cpp
	$(CXX) $(CXXFLAGS) main.cpp
clean:
	rm -f $(TARGET) $(OBJECTS)