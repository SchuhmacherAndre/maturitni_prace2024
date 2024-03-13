#include <windows.media.capture.h>
#include <wrl/client.h>
#include <wrl/wrappers/corewrappers.h>
#include <iostream>

using namespace ABI::Windows::Media::Capture;
using namespace Microsoft::WRL;

int main() {
    IActivationFactory* iaf;

    // Initialize COM
    HRESULT hr = CoInitializeEx(nullptr, COINIT_APARTMENTTHREADED);
    if (FAILED(hr)) {
        std::cerr << "Error: COM initialization failed!" << std::endl;
        return -1;
    }

    // Create MediaCapture instance
    ComPtr<IMediaCapture> mediaCapture;
    hr = iaf->ActivateInstance(Microsoft::WRL::Wrappers::HStringReference::HStringReference(RuntimeClass_Windows_Media_Capture_MediaCapture).Get(), &mediaCapture);
    if (FAILED(hr)) {
        std::cerr << "Error: Failed to create MediaCapture instance!" << std::endl;
        CoUninitialize();
        return -1;
    }

    // Initialize MediaCapture
    hr = mediaCapture->InitializeAsync().get();
    if (FAILED(hr)) {
        std::cerr << "Error: Failed to initialize MediaCapture!" << std::endl;
        CoUninitialize();
        return -1;
    }

    // Get VideoDeviceController
    ComPtr<IVideoDeviceController> videoDeviceController;
    hr = mediaCapture->VideoDeviceController(&videoDeviceController);
    if (FAILED(hr)) {
        std::cerr << "Error: Failed to get VideoDeviceController!" << std::endl;
        CoUninitialize();
        return -1;
    }

    // Set focus value (example value, may vary depending on the camera)
    double focusValue = 0.5;
    hr = videoDeviceController->SetFocusAsync(focusValue).get();
    if (FAILED(hr)) {
        std::cerr << "Error: Failed to set focus value!" << std::endl;
        CoUninitialize();
        return -1;
    }

    std::cout << "Focus set to " << focusValue << std::endl;

    // Cleanup
    mediaCapture->Close();
    CoUninitialize();
    return 0;
}
