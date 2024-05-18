LIBTINYHTM_DIR = libtinyhtm
LIBTINYHTM_LIBNAME = libtinyhtm.a

CXX = g++
CFLAGS  = -fPIC -c -I$(LIBTINYHTM_DIR)/src/tinyhtm -I$(LIBTINYHTM_DIR)/src/  -Wall -Werror


all: $(LIBTINYHTM_LIBNAME)


SRCS	=	$(wildcard $(LIBTINYHTM_DIR)/src/*.cxx)\
			$(wildcard $(LIBTINYHTM_DIR)/src/htm/*.cxx)
SRCS := $(filter-out $(LIBTINYHTM_DIR)/src/tree_count.cxx, $(SRCS))
SRCS := $(filter-out $(LIBTINYHTM_DIR)/src/tree_entry.cxx, $(SRCS))
SRCS := $(filter-out $(LIBTINYHTM_DIR)/src/htm_convert_to_hdf5.cxx, $(SRCS))


OBJS = $(SRCS:.cxx=.o)


%.o: %.cxx
	$(CXX) $(CFLAGS) -c -o $@ $<


$(LIBTINYHTM_LIBNAME): $(OBJS)
	rm -f $(LIBTINYHTM_LIBNAME)
	ar rcs $(LIBTINYHTM_LIBNAME) $(OBJS)


clean:
	rm -rf $(OBJS)
	rm -f $(LIBTINYHTM_LIBNAME) *.a *.so
