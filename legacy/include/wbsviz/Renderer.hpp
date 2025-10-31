#pragma once
#include <string>

namespace wbsviz {

class Renderer {
public:
    // engine: "dot"  format: "svg"|"pdf"|"png"|...
    static void render(const std::string& dot, const std::string& engine,
                       const std::string& format, const std::string& outPath);
};

} // namespace wbsviz
