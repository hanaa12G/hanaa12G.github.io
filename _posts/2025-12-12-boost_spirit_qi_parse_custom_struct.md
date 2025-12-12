---
layout: default
title: Using Boost Spirit Qi to parse into my struct
author: Hana Saitou (hanasou)
tags: [c++]
pinned: False
last_modified_at: 2025-12-12 03:56:27 +0700
---
# Boost Spirit Qi: Parse into user defined struct

## Problem

I have a string with format like: `"Hanasou:10, Mr.President:Unlimited"` and I
want to parse it into following structure.
```
struct LengthBoundedField {
    std::string name;
    int max_length;
    bool has_limit;
};
```

Sure we can write something that do this in less than 5 minutes. But here I am
writing this post because I thought I *somehow* implement this in a more readable
way so we can quickly check and change. Because of this I wasted my entire day!


## Spirit Qi

This is the version I have at local, I implemented one in X3 and it's easier, but
mostly similar to what I'll write next.

From documentation and example, we can write this skeleton:

```C++
#include <boost/spirit/include/qi.hpp>
#include <string>


namespace qi = boost::spirit::qi;
namespace ascii = boost::spirit::ascii;

int main() {
    using qi::char_;
    using qi::int_;
    using qi::lit;

    using Iterator = std::string::iterator;


    qi::rule<Iterator, LengthBoundedField(), ascii::space_type> field_parser = 
        (+(char_ - char_(",:")) > ':' > (int_ | lit("Unlimited")));
    auto fieldlist_parser = field_parser % ',';
    
    std::string content = "Hanasou:10, Mr.President:Unlimited";
    std::vector<LengthBoundedField> output;

    auto it = content.begin();
    qi::phrase_parse(it, content.end(), fieldlist_parser, ascii::space, output);
    return 0;
}
```

> *NOTE*: I am using g++ 12.2.0, and boost 1.87

The first error will look
```
/usr/local/include/boost/spirit/home/support/container.hpp: In instantiation of ‘struct boost::spirit::traits::container_value<LengthBoundedField, void>’:
/usr/local/include/boost/spirit/home/qi/detail/pass_container.hpp:320:66:   required from ‘bool boost::spirit::qi::detail::pass_container<F, Attr, Sequence>::dispatch_attribute(const Component&, mpl_::true_) const [with Component = boost::spirit::qi::difference<boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >, boost::spirit::qi::char_set<boost::spirit::char_encoding::standard, false, false> >; F = boost::spirit::qi::detail::fail_function<__gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >, boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >, boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> > >; Attr = LengthBoundedField; Sequence = mpl_::bool_<false>; mpl_::true_ = mpl_::bool_<true>]’
/usr/local/include/boost/spirit/home/qi/detail/pass_container.hpp:355:38:   required from ‘bool boost::spirit::qi::detail::pass_container<F, Attr, Sequence>::operator()(const Component&) const [with Component = boost::spirit::qi::difference<boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >, boost::spirit::qi::char_set<boost::spirit::char_encoding::standard, false, false> >; F = boost::spirit::qi::detail::fail_function<__gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >, boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >, boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> > >; Attr = LengthBoundedField; Sequence = mpl_::bool_<false>]’
/usr/local/include/boost/spirit/home/qi/operator/plus.hpp:65:19:   required from ‘bool boost::spirit::qi::plus<Subject>::parse_container(F) const [with F = boost::spirit::qi::detail::pass_container<boost::spirit::qi::detail::fail_function<__gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >, boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >, boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> > >, LengthBoundedField, mpl_::bool_<false> >; Subject = boost::spirit::qi::difference<boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >, boost::spirit::qi::char_set<boost::spirit::char_encoding::standard, false, false> >]’
/usr/local/include/boost/spirit/home/qi/operator/plus.hpp:87:33:   required from ‘bool boost::spirit::qi::plus<Subject>::parse(Iterator&, const Iterator&, Context&, const Skipper&, Attribute&) const [with Iterator = __gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >; Context = boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >; Skipper = boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> >; Attribute = LengthBoundedField; Subject = boost::spirit::qi::difference<boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >, boost::spirit::qi::char_set<boost::spirit::char_encoding::standard, false, false> >]’
/usr/local/include/boost/spirit/home/qi/detail/expect_function.hpp:54:33:   required from ‘bool boost::spirit::qi::detail::expect_function<Iterator, Context, Skipper, Exception>::operator()(const Component&, Attribute&) const [with Component = boost::spirit::qi::plus<boost::spirit::qi::difference<boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >, boost::spirit::qi::char_set<boost::spirit::char_encoding::standard, false, false> > >; Attribute = LengthBoundedField; Iterator = __gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >; Context = boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >; Skipper = boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> >; Exception = boost::spirit::qi::expectation_failure<__gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> > >]’
/usr/local/include/boost/spirit/home/support/algorithm/any_if.hpp:186:21:   [ skipping 8 instantiation contexts, use -ftemplate-backtrace-limit=0 to disable ]
/usr/local/include/boost/function/function_template.hpp:757:22:   required from ‘boost::function_n<R, T>::function_n(Functor, typename std::enable_if<(! std::is_integral<Functor>::value), int>::type) [with Functor = boost::spirit::qi::detail::parser_binder<boost::spirit::qi::expect_operator<boost::fusion::cons<boost::spirit::qi::plus<boost::spirit::qi::difference<boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >, boost::spirit::qi::char_set<boost::spirit::char_encoding::standard, false, false> > >, boost::fusion::cons<boost::spirit::qi::literal_char<boost::spirit::char_encoding::standard, true, false>, boost::fusion::cons<boost::spirit::qi::alternative<boost::fusion::cons<boost::spirit::qi::any_int_parser<int, 10, 1, -1>, boost::fusion::cons<boost::spirit::qi::literal_string<const char (&)[10], true>, boost::fusion::nil_> > >, boost::fusion::nil_> > > >, mpl_::bool_<false> >; R = bool; T = {__gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >&, const __gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >&, boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >&, const boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> >&}; typename std::enable_if<(! std::is_integral<Functor>::value), int>::type = int]’
/usr/local/include/boost/function/function_template.hpp:1084:27:   required from ‘boost::function<R(T ...)>::function(Functor, typename std::enable_if<(! std::is_integral<Functor>::value), int>::type) [with Functor = boost::spirit::qi::detail::parser_binder<boost::spirit::qi::expect_operator<boost::fusion::cons<boost::spirit::qi::plus<boost::spirit::qi::difference<boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >, boost::spirit::qi::char_set<boost::spirit::char_encoding::standard, false, false> > >, boost::fusion::cons<boost::spirit::qi::literal_char<boost::spirit::char_encoding::standard, true, false>, boost::fusion::cons<boost::spirit::qi::alternative<boost::fusion::cons<boost::spirit::qi::any_int_parser<int, 10, 1, -1>, boost::fusion::cons<boost::spirit::qi::literal_string<const char (&)[10], true>, boost::fusion::nil_> > >, boost::fusion::nil_> > > >, mpl_::bool_<false> >; R = bool; T = {__gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >&, const __gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >&, boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >&, const boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> >&}; typename std::enable_if<(! std::is_integral<Functor>::value), int>::type = int]’
/usr/local/include/boost/function/function_template.hpp:1125:5:   required from ‘typename std::enable_if<(! std::is_integral<Functor>::value), boost::function<R(T ...)>&>::type boost::function<R(T ...)>::operator=(Functor) [with Functor = boost::spirit::qi::detail::parser_binder<boost::spirit::qi::expect_operator<boost::fusion::cons<boost::spirit::qi::plus<boost::spirit::qi::difference<boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >, boost::spirit::qi::char_set<boost::spirit::char_encoding::standard, false, false> > >, boost::fusion::cons<boost::spirit::qi::literal_char<boost::spirit::char_encoding::standard, true, false>, boost::fusion::cons<boost::spirit::qi::alternative<boost::fusion::cons<boost::spirit::qi::any_int_parser<int, 10, 1, -1>, boost::fusion::cons<boost::spirit::qi::literal_string<const char (&)[10], true>, boost::fusion::nil_> > >, boost::fusion::nil_> > > >, mpl_::bool_<false> >; R = bool; T = {__gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >&, const __gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >&, boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >&, const boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> >&}; typename std::enable_if<(! std::is_integral<Functor>::value), boost::function<R(T ...)>&>::type = boost::function<bool(__gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >&, const __gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >&, boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >&, const boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> >&)>&]’
/usr/local/include/boost/spirit/home/qi/nonterminal/rule.hpp:191:19:   required from ‘static void boost::spirit::qi::rule<Iterator, T1, T2, T3, T4>::define(boost::spirit::qi::rule<Iterator, T1, T2, T3, T4>&, const Expr&, mpl_::true_) [with Auto = mpl_::bool_<false>; Expr = boost::proto::exprns_::expr<boost::proto::tagns_::tag::greater, boost::proto::argsns_::list2<const boost::proto::exprns_::expr<boost::proto::tagns_::tag::greater, boost::proto::argsns_::list2<const boost::proto::exprns_::expr<boost::proto::tagns_::tag::unary_plus, boost::proto::argsns_::list1<const boost::proto::exprns_::expr<boost::proto::tagns_::tag::minus, boost::proto::argsns_::list2<const boost::spirit::terminal<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >&, const boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<boost::spirit::terminal_ex<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard>, boost::fusion::vector<const char (&)[3]> > >, 0>&>, 2>&>, 1>&, boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<const char&>, 0> >, 2>&, const boost::proto::exprns_::expr<boost::proto::tagns_::tag::bitwise_or, boost::proto::argsns_::list2<const boost::spirit::terminal<boost::spirit::tag::int_>&, const boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<boost::spirit::terminal_ex<boost::spirit::tag::lit, boost::fusion::vector<const char (&)[10]> > >, 0>&>, 2>&>, 2>; Iterator = __gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >; T1 = LengthBoundedField(); T2 = boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> >, 0>; T3 = boost::spirit::unused_type; T4 = boost::spirit::unused_type; mpl_::true_ = mpl_::bool_<true>]’
/usr/local/include/boost/spirit/home/qi/nonterminal/rule.hpp:200:32:   required from ‘boost::spirit::qi::rule<Iterator, T1, T2, T3, T4>::rule(const Expr&, const std::string&) [with Expr = boost::proto::exprns_::expr<boost::proto::tagns_::tag::greater, boost::proto::argsns_::list2<const boost::proto::exprns_::expr<boost::proto::tagns_::tag::greater, boost::proto::argsns_::list2<const boost::proto::exprns_::expr<boost::proto::tagns_::tag::unary_plus, boost::proto::argsns_::list1<const boost::proto::exprns_::expr<boost::proto::tagns_::tag::minus, boost::proto::argsns_::list2<const boost::spirit::terminal<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >&, const boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<boost::spirit::terminal_ex<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard>, boost::fusion::vector<const char (&)[3]> > >, 0>&>, 2>&>, 1>&, boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<const char&>, 0> >, 2>&, const boost::proto::exprns_::expr<boost::proto::tagns_::tag::bitwise_or, boost::proto::argsns_::list2<const boost::spirit::terminal<boost::spirit::tag::int_>&, const boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<boost::spirit::terminal_ex<boost::spirit::tag::lit, boost::fusion::vector<const char (&)[10]> > >, 0>&>, 2>&>, 2>; Iterator = __gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >; T1 = LengthBoundedField(); T2 = boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> >, 0>; T3 = boost::spirit::unused_type; T4 = boost::spirit::unused_type; std::string = std::__cxx11::basic_string<char>]’
main.cpp:34:66:   required from here
/usr/local/include/boost/spirit/home/support/container.hpp:130:12: error: no type named ‘value_type’ in ‘struct LengthBoundedField’
  130 |     struct container_value
      |            ^~~~~~~~~~~~~~~
In file included from /usr/local/include/boost/spirit/home/qi/operator/kleene.hpp:20,
                 from /usr/local/include/boost/spirit/home/qi/directive/repeat.hpp:18,
                 from /usr/local/include/boost/spirit/home/qi/directive.hpp:23,
                 from /usr/local/include/boost/spirit/home/qi.hpp:20:
/usr/local/include/boost/spirit/home/qi/detail/pass_container.hpp: In instantiation of ‘bool boost::spirit::qi::detail::pass_container<F, Attr, Sequence>::dispatch_attribute(const Component&, mpl_::true_) const [with Component = boost::spirit::qi::difference<boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >, boost::spirit::qi::char_set<boost::spirit::char_encoding::standard, false, false> >; F = boost::spirit::qi::detail::fail_function<__gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >, boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >, boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> > >; Attr = LengthBoundedField; Sequence = mpl_::bool_<false>; mpl_::true_ = mpl_::bool_<true>]’:
/usr/local/include/boost/spirit/home/qi/detail/pass_container.hpp:355:38:   required from ‘bool boost::spirit::qi::detail::pass_container<F, Attr, Sequence>::operator()(const Component&) const [with Component = boost::spirit::qi::difference<boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >, boost::spirit::qi::char_set<boost::spirit::char_encoding::standard, false, false> >; F = boost::spirit::qi::detail::fail_function<__gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >, boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >, boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> > >; Attr = LengthBoundedField; Sequence = mpl_::bool_<false>]’
/usr/local/include/boost/spirit/home/qi/operator/plus.hpp:65:19:   required from ‘bool boost::spirit::qi::plus<Subject>::parse_container(F) const [with F = boost::spirit::qi::detail::pass_container<boost::spirit::qi::detail::fail_function<__gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >, boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >, boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> > >, LengthBoundedField, mpl_::bool_<false> >; Subject = boost::spirit::qi::difference<boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >, boost::spirit::qi::char_set<boost::spirit::char_encoding::standard, false, false> >]’
/usr/local/include/boost/spirit/home/qi/operator/plus.hpp:87:33:   required from ‘bool boost::spirit::qi::plus<Subject>::parse(Iterator&, const Iterator&, Context&, const Skipper&, Attribute&) const [with Iterator = __gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >; Context = boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >; Skipper = boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> >; Attribute = LengthBoundedField; Subject = boost::spirit::qi::difference<boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >, boost::spirit::qi::char_set<boost::spirit::char_encoding::standard, false, false> >]’
/usr/local/include/boost/spirit/home/qi/detail/expect_function.hpp:54:33:   required from ‘bool boost::spirit::qi::detail::expect_function<Iterator, Context, Skipper, Exception>::operator()(const Component&, Attribute&) const [with Component = boost::spirit::qi::plus<boost::spirit::qi::difference<boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >, boost::spirit::qi::char_set<boost::spirit::char_encoding::standard, false, false> > >; Attribute = LengthBoundedField; Iterator = __gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >; Context = boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >; Skipper = boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> >; Exception = boost::spirit::qi::expectation_failure<__gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> > >]’
/usr/local/include/boost/spirit/home/support/algorithm/any_if.hpp:186:21:   required from ‘bool boost::spirit::detail::any_if(const First1&, const First2&, const Last1&, const Last2&, F&, mpl_::false_) [with Pred = boost::spirit::traits::attribute_not_unused<boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >, __gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> > >; First1 = boost::fusion::cons_iterator<const boost::fusion::cons<boost::spirit::qi::plus<boost::spirit::qi::difference<boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >, boost::spirit::qi::char_set<boost::spirit::char_encoding::standard, false, false> > >, boost::fusion::cons<boost::spirit::qi::literal_char<boost::spirit::char_encoding::standard, true, false>, boost::fusion::cons<boost::spirit::qi::alternative<boost::fusion::cons<boost::spirit::qi::any_int_parser<int, 10, 1, -1>, boost::fusion::cons<boost::spirit::qi::literal_string<const char (&)[10], true>, boost::fusion::nil_> > >, boost::fusion::nil_> > > >; Last1 = boost::fusion::cons_iterator<const boost::fusion::nil_>; First2 = boost::fusion::vector_iterator<boost::fusion::vector<LengthBoundedField&>, 0>; Last2 = boost::fusion::vector_iterator<boost::fusion::vector<LengthBoundedField&>, 1>; F = boost::spirit::qi::detail::expect_function<__gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >, boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >, boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> >, boost::spirit::qi::expectation_failure<__gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> > > >; mpl_::false_ = mpl_::bool_<false>]’
/usr/local/include/boost/spirit/home/support/algorithm/any_if.hpp:201:36:   [ skipping 7 instantiation contexts, use -ftemplate-backtrace-limit=0 to disable ]
/usr/local/include/boost/function/function_template.hpp:757:22:   required from ‘boost::function_n<R, T>::function_n(Functor, typename std::enable_if<(! std::is_integral<Functor>::value), int>::type) [with Functor = boost::spirit::qi::detail::parser_binder<boost::spirit::qi::expect_operator<boost::fusion::cons<boost::spirit::qi::plus<boost::spirit::qi::difference<boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >, boost::spirit::qi::char_set<boost::spirit::char_encoding::standard, false, false> > >, boost::fusion::cons<boost::spirit::qi::literal_char<boost::spirit::char_encoding::standard, true, false>, boost::fusion::cons<boost::spirit::qi::alternative<boost::fusion::cons<boost::spirit::qi::any_int_parser<int, 10, 1, -1>, boost::fusion::cons<boost::spirit::qi::literal_string<const char (&)[10], true>, boost::fusion::nil_> > >, boost::fusion::nil_> > > >, mpl_::bool_<false> >; R = bool; T = {__gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >&, const __gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >&, boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >&, const boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> >&}; typename std::enable_if<(! std::is_integral<Functor>::value), int>::type = int]’
/usr/local/include/boost/function/function_template.hpp:1084:27:   required from ‘boost::function<R(T ...)>::function(Functor, typename std::enable_if<(! std::is_integral<Functor>::value), int>::type) [with Functor = boost::spirit::qi::detail::parser_binder<boost::spirit::qi::expect_operator<boost::fusion::cons<boost::spirit::qi::plus<boost::spirit::qi::difference<boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >, boost::spirit::qi::char_set<boost::spirit::char_encoding::standard, false, false> > >, boost::fusion::cons<boost::spirit::qi::literal_char<boost::spirit::char_encoding::standard, true, false>, boost::fusion::cons<boost::spirit::qi::alternative<boost::fusion::cons<boost::spirit::qi::any_int_parser<int, 10, 1, -1>, boost::fusion::cons<boost::spirit::qi::literal_string<const char (&)[10], true>, boost::fusion::nil_> > >, boost::fusion::nil_> > > >, mpl_::bool_<false> >; R = bool; T = {__gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >&, const __gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >&, boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >&, const boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> >&}; typename std::enable_if<(! std::is_integral<Functor>::value), int>::type = int]’
/usr/local/include/boost/function/function_template.hpp:1125:5:   required from ‘typename std::enable_if<(! std::is_integral<Functor>::value), boost::function<R(T ...)>&>::type boost::function<R(T ...)>::operator=(Functor) [with Functor = boost::spirit::qi::detail::parser_binder<boost::spirit::qi::expect_operator<boost::fusion::cons<boost::spirit::qi::plus<boost::spirit::qi::difference<boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >, boost::spirit::qi::char_set<boost::spirit::char_encoding::standard, false, false> > >, boost::fusion::cons<boost::spirit::qi::literal_char<boost::spirit::char_encoding::standard, true, false>, boost::fusion::cons<boost::spirit::qi::alternative<boost::fusion::cons<boost::spirit::qi::any_int_parser<int, 10, 1, -1>, boost::fusion::cons<boost::spirit::qi::literal_string<const char (&)[10], true>, boost::fusion::nil_> > >, boost::fusion::nil_> > > >, mpl_::bool_<false> >; R = bool; T = {__gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >&, const __gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >&, boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >&, const boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> >&}; typename std::enable_if<(! std::is_integral<Functor>::value), boost::function<R(T ...)>&>::type = boost::function<bool(__gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >&, const __gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >&, boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >&, const boost::spirit::qi::char_class<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> >&)>&]’
/usr/local/include/boost/spirit/home/qi/nonterminal/rule.hpp:191:19:   required from ‘static void boost::spirit::qi::rule<Iterator, T1, T2, T3, T4>::define(boost::spirit::qi::rule<Iterator, T1, T2, T3, T4>&, const Expr&, mpl_::true_) [with Auto = mpl_::bool_<false>; Expr = boost::proto::exprns_::expr<boost::proto::tagns_::tag::greater, boost::proto::argsns_::list2<const boost::proto::exprns_::expr<boost::proto::tagns_::tag::greater, boos
t::proto::argsns_::list2<const boost::proto::exprns_::expr<boost::proto::tagns_::tag::unary_plus, boost::proto::argsns_::list1<const boost::proto::exprns_::expr<boost::proto::tagns_::tag::minus, boost::proto::argsns_::list2<const boost::spirit::terminal<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >&, const boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<boost::spirit::terminal_ex<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard>, boost::fusion::vector<const char (&)[3]> > >, 0>&>, 2>&>, 1>&, boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<const char&>, 0> >, 2>&, const boost::proto::exprns_::expr<boost::proto::tagns_::tag::bitwise_or, boost::proto::argsns_::list2<const boost::spirit::terminal<boost::spirit::tag::int_>&, const boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<boost::spirit::terminal_ex<boost::spirit::tag::lit, boost::fusion::vector<const char (&)[10]> > >, 0>&>, 2>&>, 2>; Iterator = __gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >; T1 = LengthBoundedField(); T2 = boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> >, 0>; T3 = boost::spirit::unused_type; T4 = boost::spirit::unused_type; mpl_::true_ = mpl_::bool_<true>]’
/usr/local/include/boost/spirit/home/qi/nonterminal/rule.hpp:200:32:   required from ‘boost::spirit::qi::rule<Iterator, T1, T2, T3, T4>::rule(const Expr&, const std::string&) [with Expr = boost::proto::exprns_::expr<boost::proto::tagns_::tag::greater, boost::proto::argsns_::list2<const boost::proto::exprns_::expr<boost::proto::tagns_::tag::greater, boost::proto::argsns_::list2<const boost::proto::exprns_::expr<boost::proto::tagns_::tag::unary_plus, boost::proto::argsns_::list1<const boost::proto::exprns_::expr<boost::proto::tagns_::tag::minus, boost::proto::argsns_::list2<const boost::spirit::terminal<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >&, const boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<boost::spirit::terminal_ex<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard>, boost::fusion::vector<const char (&)[3]> > >, 0>&>, 2>&>, 1>&, boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<const char&>, 0> >, 2>&, const boost::proto::exprns_::expr<boost::proto::tagns_::tag::bitwise_or, boost::proto::argsns_::list2<const boost::spirit::terminal<boost::spirit::tag::int_>&, const boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<boost::spirit::terminal_ex<boost::spirit::tag::lit, boost::fusion::vector<const char (&)[10]> > >, 0>&>, 2>&>, 2>; Iterator = __gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >; T1 = LengthBoundedField(); T2 = boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> >, 0>; T3 = boost::spirit::unused_type; T4 = boost::spirit::unused_type; std::string = std::__cxx11::basic_string<char>]’
main.cpp:34:66:   required from here
/usr/local/include/boost/spirit/home/qi/detail/pass_container.hpp:320:66: error: no type named ‘type’ in ‘struct boost::spirit::traits::container_value<LengthBoundedField, void>’
  320 |             typedef typename traits::container_value<Attr>::type value_type;
      |                                                                  ^~~~~~~~~~
/usr/local/include/boost/spirit/home/qi/detail/pass_container.hpp:333:15: error: no type named ‘type’ in ‘struct boost::spirit::traits::container_value<LengthBoundedField, void>’
  333 |             > predicate;
      |               ^~~~~~~~~

```

I'm have zero knowledge about how this library implemented. But looking at the error
stack, the library is try to convert the parsed type, what ever is returned from
applying `+` (Plus Parser) into our structure. As our struct is not a container,
this fails. We an also think that: our `field_parser` has `LengthBoundedField` as
attribute, while whatever return by rhs of assignment, is a nested boost/std struct
to represent the parsed string result.


We will update the parser to (note that square bracket):
```C++
(+(char_ - char_(",:")) > ':' > (int_ | lit("Unlimited")))[synthesized()];
```

`synthesized` is a struct that support an overload which *help* converting from
spirit's parser type into our parser type.

```
struct synthesized {
    template<typename Attr, typename Context>
    void operator()(Attr& attr, Context& ctx) const
    {
    }
};
```

Also note that we're having a const method here. If you don't use const method
you'll have a very long error trace. 
```
/usr/local/include/boost/spirit/home/qi/nonterminal/rule.hpp:200:32:   required from ‘boost::spirit::qi::rule<Iterator, T1, T2, T3, T4>::rule(const Expr&, const std::string&) [with Expr = boost::proto::exprns_::expr<boost::proto::tagns_::tag::subscript, boost::proto::argsns_::list2<const boost::proto::exprns_::expr<boost::proto::tagns_::tag::greater, boost::proto::argsns_::list2<const boost::proto::exprns_::expr<boost::proto::tagns_::tag::greater, boost::proto::argsns_::list2<const boost::proto::exprns_::expr<boost::proto::tagns_::tag::unary_plus, boost::proto::argsns_::list1<const boost::proto::exprns_::expr<boost::proto::tagns_::tag::minus, boost::proto::argsns_::list2<const boost::spirit::terminal<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard> >&, const boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal,
boost::proto::argsns_::term<boost::spirit::terminal_ex<boost::spirit::tag::char_code<boost::spirit::tag::char_, boost::spirit::char_encoding::standard>, boost::fusion::vector<const char (&)[3]> > >, 0>&>, 2>&>, 1>&, boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<const char&>, 0> >, 2>&, const boost::proto::exprns_::expr<boost::proto::tagns_::tag::bitwise_or, boost::proto::argsns_::list2<const boost::spirit::terminal<boost::spirit::tag::int_>&, const boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<boost::spirit::terminal_ex<boost::spirit::tag::lit, boost::fusion::vector<const char (&)[10]> > >, 0>&>, 2>&>, 2>&, boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<const synthesized&>, 0> >, 2>; Iterator = __gnu_cxx::__normal_iterator<char*, std::__cxx11::basic_string<char> >; T1 = LengthBoundedField(); T2 = boost::proto::exprns_::expr<boost::proto::tagns_::tag::terminal, boost::proto::argsns_::term<boost::spirit::tag::char_code<boost::spirit::tag::space, boost::spirit::char_encoding::ascii> >, 0>; T3 = boost::spirit::unused_type; T4 = boost::spirit::unused_type; std::string = std::__cxx11::basic_string<char>]’
main.cpp:33:81:   required from here
/usr/local/include/boost/spirit/home/support/action_dispatch.hpp:135:29: error: no match for call to ‘(const synthesized) (boost::fusion::vector<std::vector<char, std::allocator<char> >, boost::optional<int> >&, boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >&, bool&)’
  135 |                   decltype(f(BOOST_SPIRIT_FAKE_CALL(A), BOOST_SPIRIT_FAKE_CALL(B)
      |                            ~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  136 |                     , BOOST_SPIRIT_FAKE_CALL(C)))
      |                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
main.cpp:19:10: note: candidate: ‘template<class Attr, class Context> void synthesized::operator()(Attr&, Context&)’
   19 |     void operator()(Attr& attr, Context& ctx)
      |          ^~~~~~~~
main.cpp:19:10: note:   template argument deduction/substitution failed:
/usr/local/include/boost/spirit/home/support/action_dispatch.hpp:135:29: note:   candidate expects 2 arguments, 3 provided
  135 |                   decltype(f(BOOST_SPIRIT_FAKE_CALL(A), BOOST_SPIRIT_FAKE_CALL(B)
      |                            ~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  136 |                     , BOOST_SPIRIT_FAKE_CALL(C)))
      |                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

The hint to fix this error lies in the line `(const synthesized) (boost::fusion::vector<std::vector<char, std::allocator<char> >, boost::optional<int> >&, boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> >&, bool&)`.
We can see the object that used to invoke the method is const, so we should create
a const method for it.



### Everything should be fixed now, what next?

Then we will try to update our parser's attribute from the parsing context. But
we don't know which type of these parameters are, and the document doesn't mention
it clearly. So I'm using the next trick: Asking the compiler about this.

```C++
template<typename T> struct analyze;

struct synthesized {
    template<typename Attr, typename Context>
    void operator()(Attr& attr, Context& ctx) const
    {
        analyze<Attr> Im_Sad;
        // analyze<Context> Im_Sad;
    }
};
```

Here we create an incomplete struct template and we'll use inside the synthesized
method. As it's incomplete template, the compiler will stop us and will yell as
us something like:
```
main.cpp:21:23: error: ‘analyze<boost::fusion::vector<std::vector<char, std::allocator<char> >, boost::optional<int> > > Im_Sad’ has incomplete type
   21 |         analyze<Attr> Im_Sad;
main.cpp:21:26: error: ‘analyze<boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> > > Im_Sad’ has incomplete type
   21 |         analyze<Context> Im_Sad;
```

Now we know attribute of `Attribute` is a `boost::fusion::vector<std::vector<char, std::allocator<char> >, boost::optional<int> >`,
and type of `Context` is a `boost::spirit::context<boost::fusion::cons<LengthBoundedField&, boost::fusion::nil_>, boost::fusion::vector<> > `


### Let's implement the rest

```C++
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
```


### Now we'll have the result

```C++
    std::string content = "Hanasou:10, Mr.President:Unlimited";
    qi::phrase_parse(it, content.end(), field_parser, ascii::space, output);
    std::cout << output << std::endl; 
    /***
        name: Hanasou, length: 10
    ***/
    
    std::string content = "Hanasou:10, Mr.President:Unlimited";
    std::vector<LengthBoundedField> outputs;

    auto it = content.begin();
    qi::phrase_parse(it, content.end(), field_parser % ',', ascii::space, outputs);

    for (auto output: output) {
        std::cout << output << std::endl;
    }
    /***
        name: Hanasou, length: 10
        name: Mr.President, length: Unlimited
    ***/
    
```


## Conclusion

I thought I'm a genius but no: This looks more complex than a regular function
that contains 2 for and 2 if. Maybe this can help with more complex parser. Anyway,
I can understand a little more about this library and it may help me in the future.

There are 3 versions of spirit and a another library with same functionality (Boost::Parser),
and I also see that 4th version of Boost::Spirit is under development. But I think
one limitation of Spirit is the documentation. With a simple use case like my example,
I cannot find the exact (best) way to do thing. LLMs didn't help too as they also
confused :D Hope someone may find this post helpful for your job in the future.
