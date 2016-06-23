CXX = g++
TARGET = sensor_ctl.cpp
CXXFLAGS = -Wall -O2 -pipe
SRCS = sensor_ctl.cpp
OBJS := $(SRCS:.cpp=.o)

$(TARGET): $(OBJS)
	$(CXX) -o $@ $(OBJS)

clean:
	rm -f $(TARGET) $(OBJS)