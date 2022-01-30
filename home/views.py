from django.shortcuts import render
from django.http import HttpResponse
import azure.cognitiveservices.speech as speechsdk
from sqlalchemy import null

# Create your views here.


def index(request):

    return render(request, 'index.html')


def imgurl(request):
    url = ""
    if request.method == 'POST':
        url = request.POST['imgurl']
        import requests

        subscription_key = "2af2508f2b484dde8643005928af8820"

        endpoint = "https://test-cv-28jan.cognitiveservices.azure.com/"

        ocr_url = endpoint + "vision/v3.1/ocr"

        # Set image_url to the URL of an image that you want to analyze.
        image_url = url

        headers = {'Ocp-Apim-Subscription-Key': subscription_key}
        params = {'language': 'unk', 'detectOrientation': 'true'}
        data = {'url': image_url}
        response = requests.post(
            ocr_url, headers=headers, params=params, json=data)
        response.raise_for_status()

        analysis = response.json()
        strtext = ""
        # Extract the word bounding boxes and text.
        line_infos = [region["lines"] for region in analysis["regions"]]
        word_infos = []
        for line in line_infos:
            for word_metadata in line:
                for word_info in word_metadata["words"]:
                    word_infos.append(word_info)
        word_infos
        for dic in word_infos:
            strtext = strtext+" "+dic.get('text')
        print(word_infos)

        params = {'text': strtext, 'url': url}
        return render(request, 'raitext.html', params)
    elif request.GET['urlimg'] != null:
        url = request.GET['urlimg']
        import requests

        # Add your Computer Vision subscription key and endpoint to your environment variables.
        subscription_key = "2af2508f2b484dde8643005928af8820"

        endpoint = "https://test-cv-28jan.cognitiveservices.azure.com/"

        ocr_url = endpoint + "vision/v3.1/ocr"

        # Set image_url to the URL of an image that you want to analyze.
        image_url = url

        headers = {'Ocp-Apim-Subscription-Key': subscription_key}
        params = {'language': 'unk', 'detectOrientation': 'true'}
        data = {'url': image_url}
        response = requests.post(
            ocr_url, headers=headers, params=params, json=data)
        response.raise_for_status()

        analysis = response.json()
        strtext = ""
        # Extract the word bounding boxes and text.
        line_infos = [region["lines"] for region in analysis["regions"]]
        word_infos = []
        for line in line_infos:
            for word_metadata in line:
                for word_info in word_metadata["words"]:
                    word_infos.append(word_info)
        word_infos
        for dic in word_infos:
            strtext = strtext+" "+dic.get('text')
        print(word_infos)

        params = {'text': strtext, 'url': url}
        return render(request, 'raitext.html', params)
    else:
        return render(request, 'index.html')


def readtext(request):
    if request.method == 'POST':
        text = request.POST['strtext']
        speech_key, service_region = "f22c3f0ad7234f399f1f8956499f85fc", "eastus"
        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key, region=service_region)

        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config)

        result = speech_synthesizer.speak_text_async(text).get()

        # Checks result.
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized to speaker for text [{}]".format(text))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(
                cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(
                        cancellation_details.error_details))
            print("Did you update the subscription info?")
        return render(request, 'index.html')
    else:
        return render(request, 'index.html')
