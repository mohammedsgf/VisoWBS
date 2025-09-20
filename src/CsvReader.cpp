#include "wbsviz/CsvReader.hpp"
#include "wbsviz/Common.hpp"
#include <fstream>
#include <stdexcept>

namespace wbsviz {

CsvReader::CsvReader(std::string path) : path_(std::move(path)) {}

std::vector<Record> CsvReader::read() const {
    std::ifstream in(path_);
    if (!in) throw std::runtime_error("Failed to open CSV: " + path_);

    std::string hdr; if(!std::getline(in,hdr)) throw std::runtime_error("Empty CSV");
    auto H = splitCsvLine(hdr);
    for (auto& h: H) h = toLower(h);

    auto idx = [&](const std::string& k)->int{
        auto kl = toLower(k);
        for (size_t i=0;i<H.size();++i) if (H[i]==kl) return static_cast<int>(i);
        return -1;
    };
    const int i_code=idx("code"), i_title=idx("title"),
              i_owner=idx("owner"), i_status=idx("status"),
              i_start=idx("start"), i_end=idx("end"), i_est=idx("estimate");

    if (i_code<0 || i_title<0) throw std::runtime_error("CSV missing required headers: code,title");

    std::vector<Record> out; std::string line; size_t ln=1;
    while (std::getline(in,line)) {
        ++ln; if(line.empty()) continue;
        auto row = splitCsvLine(line);
        auto get = [&](int i)->std::string { return (i>=0 && i < (int)row.size()) ? row[i] : std::string{}; };
        Record r;
        r.code=get(i_code); r.title=get(i_title);
        r.owner=get(i_owner); r.status=get(i_status);
        r.start=get(i_start); r.end=get(i_end);
        r.estimate=get(i_est);
        if (r.code.empty() || r.title.empty())
            throw std::runtime_error("Missing code/title at line " + std::to_string(ln));
        out.push_back(std::move(r));
    }
    return out;
}

} // namespace wbsviz
