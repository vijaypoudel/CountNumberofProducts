
import openai

from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

OPENAI_API_KEY = "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"
OPENAI_ORGANIZATION = "org-OlqyyAtuOKUxIEkl6rvsTabb"

@app.route('/test', methods=['GET'])
def test():
    return "hello there Vijay "


@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    data = request.json
    image_url = data.get('image_url')

    if not image_url:
        ret = '{"error": "No image URL provided"}'
        resp = Response(response=ret,
                    status=401,
                    mimetype="application/json")
        return resp

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY, organization=OPENAI_ORGANIZATION)
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Formet your whole response in JSON format. You are an API, who only responds in JSON foramt. No description or context is added to your response. Now here is the context in which you will respond. From a given list of products we need to identify in the image and return back a json response with the name of the item ( key : item )and number of product ( key : numberOfProduct). The list if Pepsi, Cadbury, Maggi. Skip the item from the response if it is not there in the image. The response should be in JSON Format so that it can work with jsonify"},
                        {
                            "type": "image_url",
                            "image_url": image_url,
                        },
                    ],
                }
            ],
            max_tokens=1000,
        )

        if response.choices:
            return jsonify({"result": response.choices[0].message.content})
        else:
            return jsonify({"error": "No response from OpenAI"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
