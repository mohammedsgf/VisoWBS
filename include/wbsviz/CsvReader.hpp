#pragma once
#include <string>
#include <vector>
#include "Model.hpp"

namespace wbsviz {

class CsvReader {
public:
    explicit CsvReader(std::string path);
    std::vector<Record> read() const;
private:
    std::string path_;
};

} // namespace wbsviz
