CXX = g++
TARGET = sample.cpp
CXXFLAGS = -Wall -O2 -pipe
SRCS = sample.cpp
OBJS := $(SRCS:.cpp=.o)

$(TARGET): $(OBJS)
	$(CXX) -o $@ $(OBJS)

clean:
	rm -f $(TARGET) $(OBJS)