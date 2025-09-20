cmake_minimum_required(VERSION 3.16)
project(wbsviz LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Try pkg-config first
find_package(PkgConfig QUIET)
if (PkgConfig_FOUND)
  pkg_check_modules(GVC QUIET libgvc)
  pkg_check_modules(CGRAPH QUIET libcgraph)
endif()

if (GVC_FOUND AND CGRAPH_FOUND)
  set(GV_INCLUDE_DIRS ${GVC_INCLUDE_DIRS} ${CGRAPH_INCLUDE_DIRS})
  set(GV_LIBS ${GVC_LINK_LIBRARIES} ${CGRAPH_LINK_LIBRARIES})
else()
  # Fallback manual discovery
  find_path(GRAPHVIZ_INCLUDE_DIR
    NAMES gvc.h cgraph.h
    PATH_SUFFIXES graphviz
  )
  find_library(GVC_LIB NAMES gvc)
  find_library(CGRAPH_LIB NAMES cgraph)
  if (NOT GRAPHVIZ_INCLUDE_DIR OR NOT GVC_LIB OR NOT CGRAPH_LIB)
    message(FATAL_ERROR "Graphviz dev libraries not found. Install libgraphviz-dev / graphviz-devel")
  endif()
  set(GV_INCLUDE_DIRS ${GRAPHVIZ_INCLUDE_DIR})
  set(GV_LIBS ${GVC_LIB} ${CGRAPH_LIB})
endif()

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

add_library(wbsviz_core
  src/CsvReader.cpp
  src/TreeBuilder.cpp
  src/DotBuilder.cpp
  src/Renderer.cpp
)
target_include_directories(wbsviz_core PRIVATE ${GV_INCLUDE_DIRS})
target_link_libraries(wbsviz_core PRIVATE ${GV_LIBS})

add_executable(wbsviz src/main.cpp)
target_include_directories(wbsviz PRIVATE ${GV_INCLUDE_DIRS})
target_link_libraries(wbsviz PRIVATE wbsviz_core ${GV_LIBS})
