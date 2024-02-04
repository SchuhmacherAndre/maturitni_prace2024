#define _CRT_SECURE_NO_WARNINGS

#include <cstdint>
#include <iostream>
#include <vector>
#include <cassert>
#include <future>

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


using bsoncxx::builder::basic::kvp;
using bsoncxx::builder::basic::make_array;
using bsoncxx::builder::basic::make_document;

mongocxx::database db{};
mongocxx::collection collection{};

crow::SimpleApp webApp{};
std::future<void> webRes{};

PaStream* micStream{};
float currentAudioLevel{0};

bool gameActive = false;



int endpoints()
{
	CROW_ROUTE(webApp, "/comm")
		([] {
		crow::json::wvalue x({ {"message", "hello"}});
			return x;
		});

	return 0;
}

#define SAMPLE_RATE 44100
#define FRAMES_PER_BUFFER 256

int paCallback(const void* inputBuffer, void* outputBuffer,
	unsigned long framesPerBuffer,
	const PaStreamCallbackTimeInfo* timeInfo,
	PaStreamCallbackFlags statusFlags,
	void* userData) {


	float* input = (float*)inputBuffer;
	long double power = 0.0;

	// Calculate power of the audio signal
	for (unsigned long i = 0; i < framesPerBuffer; i++) {
		power += static_cast<long double>(input[i]) * static_cast<long double>(input[i]);
	}

	// Normalize the power by the number of samples
	power /= framesPerBuffer;

	// Convert power to decibels using log10l for long double precision
	long double power_dB = 10 * log10l(power);

	currentAudioLevel = power_dB;

	return paContinue;
}

int main(int argc, char* argv[])
{
	// Logging Setup
	loguru::init(argc, argv);
	loguru::add_file("everything.log", loguru::Append, loguru::Verbosity_MAX);
	loguru::g_stderr_verbosity = 1;

	LOG_F(INFO, "WELCOME to DARTS");
	LOG_F(INFO, "Establishing connection to Darts DB...");

	// Try establishing connection to mongodb, our DB & collection.
	try {
		mongocxx::instance instance{};
		mongocxx::client client{ mongocxx::uri{} };

		// exception... if not running.. lol
		client.list_databases().begin();

		db = client["darts"];
		collection = db["myCollection"];
	}
	catch (const std::exception &ex) {
		LOG_F(ERROR, "%s", ex.what());
		return 0;
	}

	LOG_F(INFO, "Established connection to Darts DB.");
	LOG_F(INFO, "Establishing connection to Webserver...");

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
	LOG_F(INFO, "Starting Port Audio..");

	std::async(std::launch::async, [&] {
		try {
			freopen("null", "w", stderr); // little hack to disable output from portaudio.. pointless
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
	LOG_F(INFO, "Starting Main loop..");

	// main loop, non blocking.
	std::thread([] {
		while (true) {
			if (!gameActive) return;
			// dart landing check logic goes here

			// detect dart logic goes here

			// upload values to webserver here

			// we go again
			
			std::this_thread::sleep_for(std::chrono::milliseconds(500));
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