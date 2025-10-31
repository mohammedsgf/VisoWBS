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
    for (auto& h: H) h = toLower(h);  // case-insensitive headers

    auto idx = [&](const std::string& k)->int{
        auto kl = toLower(k);
        for (size_t i=0;i<H.size();++i) if (H[i]==kl) return static_cast<int>(i);
        return -1;
    };

    // Required headers
    const int i_code  = idx("code");
    const int i_title = idx("title");
    if (i_code<0 || i_title<0)
        throw std::runtime_error("CSV missing required headers: code,title");

    //Optional
    const int i_desc  = idx("description");
    const int i_pr    = idx("primaryresp");
    const int i_sr    = idx("seconderyresp");   
    const int i_est   = idx("estimateduration");

    std::vector<Record> out; std::string line; size_t ln=1;
    while (std::getline(in,line)) {
        ++ln; if(line.empty()) continue;
        auto row = splitCsvLine(line);
        auto get = [&](int i)->std::string { return (i>=0 && i < (int)row.size()) ? row[i] : std::string{}; };

        Record r;
        r.code            = get(i_code);
        r.title           = get(i_title);
        r.description     = get(i_desc);
        r.primaryResp     = get(i_pr);
        r.seconderyResp   = get(i_sr);
        r.estimateDuration= get(i_est);

        if (r.code.empty() || r.title.empty())
            throw std::runtime_error("Missing code/title at line " + std::to_string(ln));

        out.push_back(std::move(r));
    }
    return out;
}

} // namespace wbsviz
