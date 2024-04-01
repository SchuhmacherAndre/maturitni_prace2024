#define _CRT_SECURE_NO_WARNINGS

#include <print>
#include <cstdint>
#include <iostream>
#include <vector>
#include <cassert>
#include <future>
#include <string>
#include <sstream>

#include <zmq.hpp>
#include <loguru.hpp>
#include <loguru.cpp>
#include <crow.h>
#include <bsoncxx/builder/basic/document.hpp>
#include <bsoncxx/json.hpp>
#include <mongocxx/client.hpp>
#include <mongocxx/instance.hpp>
#include <mongocxx/stdx.hpp>
#include <mongocxx/uri.hpp>
#include <portaudio.h>


#include <Windows.h>

#define SAMPLE_RATE 44100
#define FRAMES_PER_BUFFER 256

using bsoncxx::builder::basic::kvp;
using bsoncxx::builder::basic::make_array;
using bsoncxx::builder::basic::make_document;

mongocxx::database db{};
mongocxx::collection collection{};

crow::SimpleApp webApp{};
std::future<void> webRes{};

PaStream* micStream{};
float currentAudioLevel{0};

bool gameActive = true;
bool dartImpact = false;
bool go = true;

std::vector<float> dartImpactArr{};



int endpoints()
{
	CROW_ROUTE(webApp, "/comm")
		([] {
		crow::json::wvalue x({ {"message", "hello"}});
			return x;
		});

	return 0;
}

int paCallback(const void* inputBuffer, void* outputBuffer,
	unsigned long framesPerBuffer,
	const PaStreamCallbackTimeInfo* timeInfo,
	PaStreamCallbackFlags statusFlags,
	void* userData) {


	float* input = (float*)inputBuffer;
	long double power = 0.0;

	// calc power of audio signal
	for (unsigned long i = 0; i < framesPerBuffer; i++) {
		power += static_cast<long double>(input[i]) * static_cast<long double>(input[i]);
	}

	// normalization calculation
	power /= framesPerBuffer;

	// power to decibel conversion
	long double power_dB = 10 * log10l(power);

	currentAudioLevel = power_dB;

	return paContinue;
}

std::string removeFirstXLines(const std::string& input, int x) {
	size_t pos = 0;
	for (int i = 0; i < x; ++i) {
		pos = input.find('\n', pos);
		if (pos == std::string::npos) // Less than x lines
			return "";
		++pos; // Move past the newline character
	}
	return input.substr(pos);
}

std::string getPoints()
{
	// invoke python script
	LOG_F(INFO, "trying to invoke script..");
	FILE* pipe = _popen("python pred2.py", "r");
	if (!pipe) {
		std::cerr << "Error: Couldn't invoke getPoints script." << std::endl;
		return "NULL";
	}
	// Buffer to store the output of the Python script
	constexpr int MAX_BUFFER = 1024;
	char buffer[MAX_BUFFER];

	// Read output from the Python script
	std::string output;
	while (!feof(pipe)) {
		if (fgets(buffer, MAX_BUFFER, pipe) != nullptr) 
			output += buffer;
		
	}
	// Close the pipe
	_pclose(pipe);
	

	return output;
}


int main(int argc, char* argv[])
{
	// Logging Setup
	loguru::init(argc, argv);
	loguru::add_file("everything.log", loguru::Append, loguru::Verbosity_MAX);
	loguru::g_stderr_verbosity = 1;

	LOG_F(INFO, "WELCOME to DARTS");

	// Try establishing connection to mongodb, our DB & collection.
	//try {
	//	mongocxx::instance instance{};
	//	mongocxx::client client{ mongocxx::uri{} };

	//	// exception... if not running.. lol
	//	client.list_databases().begin();

	//	db = client["darts"];
	//	collection = db["mycollection"];
	//}
	//catch (const std::exception &ex) {
	//	log_f(error, "%s", ex.what());
	//	return 0;
	//}

	// LOG_F(INFO, "Established connection to Darts DB.");

	// Try creating our endpoints and running our async (non blocking) webserver.
	try {
		endpoints();

		webApp.loglevel(crow::LogLevel::Critical);
		webRes = webApp.port(17777).run_async(); // port 17777 for goodluck
	}
	catch (const std::exception& ex) {
		LOG_F(ERROR, "%s", ex.what());
		return 0;
	}

	LOG_F(INFO, "Webserver running @ http://0.0.0.0:17777.");

	std::async(std::launch::async, [&] {
		try {
			freopen("null", "w", stderr); // little hack to disable output from portaudio..
			Pa_Initialize();
			Pa_OpenDefaultStream(&micStream,
				1,         
				0,         
				paFloat32, 
				SAMPLE_RATE,
				FRAMES_PER_BUFFER,
				paCallback,
				nullptr);
			Pa_StartStream(micStream);
			freopen("CON", "w", stderr); // re-enable stderr channel
		}
		catch (const std::exception& ex) {
			LOG_F(ERROR, "%s", ex.what());
			return 0;
		}
	});

	LOG_F(INFO, "Port Audio started.");


	// dart impact check loop
	std::thread([] {
		while (true) {
		
			if (currentAudioLevel >= -25.f) {
				dartImpact = true;
			}			

			else {
				dartImpact = false;
			}
		}

	}).detach();

	Sleep(1000);

	LOG_F(INFO, "Dart Impact loop started.");

	// main loop, non blocking.
	std::thread([] {
		while (true) {
			Sleep(50);
			if (!gameActive) continue;
			if (!dartImpact) continue;

			LOG_F(WARNING, "IMPACT");
		
			getPoints();
			std::print("done");

			
		}
	}).detach();

	LOG_F(INFO, "Main loop started.");
	
	

	

	/*auto cursor_all = collection.find({});
	std::cout << "collection " << collection.name()
		<< " contains these documents:" << std::endl;
	for (auto doc : cursor_all) {
		std::cout << bsoncxx::to_json(doc, bsoncxx::ExtendedJsonMode::k_relaxed) << std::endl;
	}
	std::cout << std::endl;
	*/


	// Try getting webRes result, so that it doesn't block anything
	try {
		webRes.get();
	}
	catch (const std::exception& ex) {
		LOG_F(ERROR, "%s", ex.what());
		return 0;
	}

	return 0;


}