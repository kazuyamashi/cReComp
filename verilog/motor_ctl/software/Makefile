CXX = g++
TARGET = motor_ctl
CXXFLAGS = -Wall -O2 -pipe
SRCS = motor_ctl.cpp
OBJS := $(SRCS:.cpp=.o)

$(TARGET): $(OBJS)
	$(CXX) -o $@ $(OBJS)

clean:
	rm -f $(TARGET) $(OBJS)