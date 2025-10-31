#include <algorithm>
#include <fstream>
#include <iostream>
#include <optional>
#include <string>

#include "wbsviz/CsvReader.hpp"
#include "wbsviz/TreeBuilder.hpp"
#include "wbsviz/DotBuilder.hpp"
#include "wbsviz/Renderer.hpp"

static std::optional<std::string> argVal(int argc, char** argv, const std::string& flag){
    for(int i=1;i<argc-1;++i) if (argv[i]==flag) return std::string(argv[i+1]); return std::nullopt;
}
static void usage(const char* p){
    std::cerr << "Usage:\n  " << p << " --in wbs.csv [--out diagram.svg] [--format svg|pdf|png|dot] [--rankdir TB|LR] [--strict true|false]\n";
}

int main(int argc, char** argv){
    std::string in, out="diagram.svg", format="svg", rankdir="TB";
    bool strict=true;
    if (auto v=argVal(argc,argv,"--in")) in=*v;
    if (auto v=argVal(argc,argv,"--out")) out=*v;
    if (auto v=argVal(argc,argv,"--format")) format=*v;
    if (auto v=argVal(argc,argv,"--rankdir")) rankdir=*v;
    if (auto v=argVal(argc,argv,"--strict")) { auto s=*v; std::transform(s.begin(),s.end(),s.begin(),::tolower); strict = (s=="true"||s=="1"||s=="yes"||s=="y"); }

    if (in.empty() || (format!="svg"&&format!="pdf"&&format!="png"&&format!="dot")) { usage(argv[0]); return 1; }

    try{
        wbsviz::CsvReader reader(in);
        auto recs = reader.read();

        wbsviz::TreeBuilder builder(strict);
        auto tree = builder.build(recs);

        wbsviz::DotBuilder dotb(rankdir);
        auto dot = dotb.build(tree);

        if (format=="dot") {
            std::ofstream f(out); if(!f) throw std::runtime_error("Open out failed: "+out);
            f << dot;
            std::cerr << "Wrote DOT to " << out << "\n";
        } else {
            wbsviz::Renderer::render(dot, "dot", format, out);
            std::cerr << "Wrote " << format << " to " << out << "\n";
        }
        return 0;
    } catch (const std::exception& e){
        std::cerr << "[ERROR] " << e.what() << "\n";
        return 1;
    }
}
