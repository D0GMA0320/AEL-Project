# What to enter in Configure services

Double-click `configure-services.cmd` in the project folder. Enter the four **values**, without typing `NAME=` or quotation marks. Secret key prompts do not show the characters you type/paste. Pressing Enter on a blank entry keeps its previous value, if any.

For each key, copy the complete key using the provider's copy button, then type **C** at the clipboard/input choice and press Enter. The script reads the clipboard without displaying the secret. Alternatively, press Enter to use hidden input. Some Windows consoles do not paste correctly with Ctrl+V into a hidden prompt; clipboard mode avoids that problem. Incomplete keys are rejected, including invalid previously saved keys. Keep the Azure region and OpenAI model fields as ordinary text input.

| Prompt | Value to enter | Where to find it |
| --- | --- | --- |
| `SPEECH_KEY` | One Azure Speech resource key: KEY 1 or KEY 2 | [Azure portal](https://portal.azure.com/) → your Speech resource → **Keys and Endpoint** |
| `SPEECH_REGION` | The region code for that same resource, such as `koreacentral` or `eastus` | The resource's **Location/Region**. It must match where you created the resource. Enter the code, not `Korea Central`, an endpoint URL, or `en-AU`. |
| `OPENAI_API_KEY` | Your OpenAI API project's secret key | [OpenAI API keys](https://platform.openai.com/api-keys) → choose your project → create/copy a secret key. This is not your ChatGPT password or Azure key. |
| `OPENAI_MODEL` | An exact API model ID, for example `gpt-5.4-mini` if available to your project | Your API project's available models. This is a model identifier, not a credential. GPT-5.4 mini supports the Responses API used by this application. |

This application uses a regional Azure endpoint constructed from `SPEECH_REGION`; it does not currently ask for an endpoint URL. The region controls the Azure resource connection, **not the spoken accent**. US/UK/AU are chosen in the app.

You need an Azure resource with usable Speech quota and an OpenAI API project able to make the selected model's requests. Logging into ChatGPT alone does not supply the API key this app needs. Check the API project's usage/billing settings before testing.

The setup writes a local `.env` file, excluded from Git and the portable ZIP. It checks key format locally but does not verify service access or make paid requests. Do not paste secrets into a chat or screen recording.

After saving:

1. Run `prepare-classroom.cmd` to generate Azure MP3s and rebuild the classroom ZIP.
2. Run `start-classroom.cmd` for live AI feedback, then open `http://127.0.0.1:8765`.
3. If the server was already open, restart it to reload the settings.

The provider settings remain optional for static quizzes and prepared explanations. Do not enter fake/example keys; leave unavailable services blank.

References checked November 24, 2026: [Azure Speech regions](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/regions), [Azure Speech private endpoint guide — Keys and Endpoint location](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-services-private-link), [OpenAI quickstart](https://developers.openai.com/api/docs/quickstart), [GPT-5.4 mini](https://developers.openai.com/api/docs/models/gpt-5.4-mini).
