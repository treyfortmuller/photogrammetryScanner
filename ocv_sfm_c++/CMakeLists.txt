cmake_minimum_required( VERSION 2.8 )
project( mirror_pivot_sfm )

### LIBMV LIGHT EXTERNAL DEPENDENCIES ###
find_package( Eigen 3 QUIET )
if( NOT Eigen_FOUND )
    include( /usr/share/cmake-2.8/Modules/FindEigen3.cmake )
    set( Eigen_INCLUDE_DIR ${EIGEN3_INCLUDE_DIR} )
endif()
find_package(Gflags QUIET)
find_package(Ceres QUIET)
if(NOT Ceres_FOUND)  # Looks like Ceres find glog on the own, so separate search isn't necessary
    find_package(Glog QUIET)
endif()

include_directories( ~/opencv_contrib/modules/sfm/include )
include_directories( ${Eigen_INCLUDE_DIR} )

if((gflags_FOUND OR GFLAGS_FOUND) AND (glog_FOUND OR GLOG_FOUND))
    set(_fname "${CMAKE_CURRENT_BINARY_DIR}/test_sfm_deps.cpp")
    file(WRITE "${_fname}" "#include <glog/logging.h>\n#include <gflags/gflags.h>\nint main() { (void)(0); return 0; }\n")
    try_compile(SFM_DEPS_OK "${CMAKE_BINARY_DIR}" "${_fname}"
            CMAKE_FLAGS "-DINCLUDE_DIRECTORIES:STRING=${GLOG_INCLUDE_DIRS};${GFLAGS_INCLUDE_DIRS}"
            LINK_LIBRARIES ${GLOG_LIBRARIES} ${GFLAGS_LIBRARIES}
            OUTPUT_VARIABLE OUTPUT
            )
    file(REMOVE "${_fname}")
    message(STATUS "Checking SFM deps... ${SFM_DEPS_OK}")
else()
    set(SFM_DEPS_OK FALSE)
endif()

if(NOT HAVE_EIGEN OR NOT SFM_DEPS_OK)
    set(DISABLE_MSG "MODULE OPENCV_SFM DISABLED: the following dependencies are not found:")
    if(NOT HAVE_EIGEN)
        set(DISABLE_MSG "${DISABLE_MSG} Eigen")
    endif()
    if(NOT SFM_DEPS_OK)
        set(DISABLE_MSG "${DISABLE_MSG} Glog/Gflags")
    endif()
    message(STATUS ${DISABLE_MSG})
endif()


### LIBMV LIGHT DEFINITIONS ###

set(LIBMV_LIGHT_INCLUDES
        src/libmv_light
        "${OpenCV_SOURCE_DIR}/include/opencv"
        "${GLOG_INCLUDE_DIRS}"
        "${GFLAGS_INCLUDE_DIRS}"
        )

set(LIBMV_LIGHT_LIBS
        correspondence
        multiview
        numeric
        ${GLOG_LIBRARIES}
        ${GFLAGS_LIBRARIES}
        )

if(Ceres_FOUND)
    add_definitions("-DCERES_FOUND=1")
    list(APPEND LIBMV_LIGHT_LIBS simple_pipeline)
    list(APPEND LIBMV_LIGHT_INCLUDES "${CERES_INCLUDE_DIR}")
else()
    add_definitions("-DCERES_FOUND=0")
    message(STATUS "CERES support is disabled. Ceres Solver for reconstruction API is required.")
endif()


add_executable( mirror_pivot_sfm main.cpp )
target_link_libraries( mirror_pivot_sfm ${OpenCV_LIBS} ${CERES_LIBRARIES} )




