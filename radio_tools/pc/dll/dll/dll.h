#ifndef _DLL_H_
#define _DLL_H_

#ifdef BUILD_DLL
    #define DLL_EXPORT __declspec(dllexport)
#else
    #define DLL_EXPORT __declspec(dllimport)
#endif

#endif // _DLL_H_

