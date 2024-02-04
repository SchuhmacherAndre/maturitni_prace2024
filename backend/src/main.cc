#include <cstdint>
#include <iostream>
#include <vector>
#include <cassert>


#include <loguru.hpp>
#include <loguru.cpp>
#include <bsoncxx/builder/basic/document.hpp>
#include <bsoncxx/json.hpp>
#include <mongocxx/client.hpp>
#include <mongocxx/instance.hpp>
#include <mongocxx/stdx.hpp>
#include <mongocxx/uri.hpp>


using bsoncxx::builder::basic::kvp;
using bsoncxx::builder::basic::make_array;
using bsoncxx::builder::basic::make_document;


int main(int argc, char* argv[])
{
	loguru::init(argc, argv);
	loguru::add_file("everything.log", loguru::Append, loguru::Verbosity_MAX);
	loguru::g_stderr_verbosity = 1;

	LOG_F(INFO, "hello world");
	LOG_F(INFO, "establishing connection to DB...");
	mongocxx::instance instance{}; // This should be done only once.
	mongocxx::client client{ mongocxx::uri{} };
	auto db = client["darts"];
	auto collection = db["myCollection"];

	auto cursor_all = collection.find({});
	std::cout << "collection " << collection.name()
		<< " contains these documents:" << std::endl;
	for (auto doc : cursor_all) {
		std::cout << bsoncxx::to_json(doc, bsoncxx::ExtendedJsonMode::k_relaxed) << std::endl;
	}
	std::cout << std::endl;




	return 0;


}