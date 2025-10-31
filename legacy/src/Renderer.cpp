#include "wbsviz/Renderer.hpp"
#include <stdexcept>

// Prefer robust include path; CMake adds /usr/include/graphviz for you
#include <graphviz/gvc.h>
#include <graphviz/cgraph.h>

namespace wbsviz {

class GvcCtx {
public:
    GvcCtx() : ctx_(gvContext()) { if(!ctx_) throw std::runtime_error("gvContext() failed"); }
    ~GvcCtx(){ gvFreeContext(ctx_); }
    GVC_t* get() const { return ctx_; }
private:
    GVC_t* ctx_;
};

class GraphMem {
public:
    explicit GraphMem(const std::string& dot) : g_(agmemread(dot.c_str())) {
        if(!g_) throw std::runtime_error("agmemread() failed to parse DOT");
    }
    ~GraphMem(){ agclose(g_); }
    Agraph_t* get() const { return g_; }
private:
    Agraph_t* g_;
};

void Renderer::render(const std::string& dot, const std::string& engine,
                      const std::string& format, const std::string& outPath) {
    GvcCtx gvc;
    GraphMem g(dot);
    if (gvLayout(gvc.get(), g.get(), engine.c_str()) != 0)
        throw std::runtime_error("gvLayout() failed (engine=" + engine + ")");
    if (gvRenderFilename(gvc.get(), g.get(), format.c_str(), outPath.c_str()) != 0) {
        gvFreeLayout(gvc.get(), g.get());
        throw std::runtime_error("gvRenderFilename() failed (format=" + format + ")");
    }
    gvFreeLayout(gvc.get(), g.get());
}

} // namespace wbsviz
