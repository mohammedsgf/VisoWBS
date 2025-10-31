#pragma once
#include <string>
#include <vector>
#include <regex>
#include <sstream>

namespace wbsviz {

inline std::vector<std::string> splitCsvLine(const std::string& line) {
    std::vector<std::string> f; std::string cur; bool q=false;
    for (size_t i=0;i<line.size();++i) {
        char c=line[i];
        if (c=='"') { if (q && i+1<line.size() && line[i+1]=='"'){cur.push_back('"');++i;} else q=!q; }
        else if (c==',' && !q) { f.push_back(cur); cur.clear(); }
        else cur.push_back(c);
    }
    f.push_back(cur);
    return f;
}

inline bool validCode(const std::string& c) {
    static const std::regex re(R"(^\d+(\.\d+)*$)");
    return std::regex_match(c, re);
}

inline std::string parentCode(const std::string& c) {
    auto p = c.find_last_of('.');
    return p==std::string::npos ? std::string{} : c.substr(0,p);
}

inline std::string toLower(std::string s){ for(char& c:s) c=char(::tolower(c)); return s; }

inline std::string esc(const std::string& in){
    std::string out; out.reserve(in.size()+8);
    for(char c:in){ if(c=='\\'||c=='"') out.push_back('\\'); out.push_back(c); }
    return out;
}

} // namespace wbsviz
