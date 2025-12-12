#include <boost/spirit/include/qi.hpp>
#include <string>


struct LengthBoundedField {
    std::string name;
    int max_length;
    bool has_limit;
};

std::ostream& operator<<(std::ostream& os, LengthBoundedField const& f) {
    os << "name: " << f.name;
    if (!f.has_limit) {
        os << ", length: Unlimited";
    }
    else {
        os << ", length: " << f.max_length;
    }

    return os;
}


namespace qi = boost::spirit::qi;
namespace ascii = boost::spirit::ascii;

template<typename T> struct analyze;

struct synthesized {
    template<typename Attr, typename Context>
    void operator()(Attr& attr, Context& ctx) const
    {
        using boost::fusion::at_c;

        auto& out = at_c<0>(ctx.attributes);
        
        auto const& first = at_c<0>(attr);
        out.name = std::string ( first.begin(), first.end() );

        auto const& second = at_c<1>(attr);
        if (second) {
            out.has_limit = true;
            out.max_length = second.value();
        }
        else {
            out.has_limit = false;
        }
    }
};

int main() {
    using qi::char_;
    using qi::int_;
    using qi::lit;

    using Iterator = std::string::iterator;


    qi::rule<Iterator, LengthBoundedField(), ascii::space_type> field_parser = 
        (+(char_ - char_(",:")) > ':' > (int_ | lit("Unlimited")))[synthesized()];
    
    std::string content = "Hanasou:10, Mr.President:Unlimited";
    std::vector<LengthBoundedField> outputs;

    auto it = content.begin();
    qi::phrase_parse(it, content.end(), field_parser % ',', ascii::space, outputs);

    for (auto output: outputs) {
        std::cout << output << std::endl;
    }
    return 0;
}

