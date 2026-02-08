Consolidated AI Threat Assessment: Focus on SCIM Integrity & Specified Hardware Capabilities
I. Introduction
This report consolidates findings from previous research on AI Romantic/Sexual Companion Apps, AI Image/Video Generation tools, and AI Text/Code Generation platforms. The primary objective is to analyze these AI categories based on their potential threat to "SCIM" – interpreted here as the security, integrity, and ethical operation of systems, companies, infrastructure, or management processes.
The analysis will rank AI tool categories by their threat level, considering:
* Deviation from standard content policies (e.g., generating NSFW or illegal content).
* Capability for malicious code generation.
* Susceptibility to prompt manipulation and "puppetry."
* Ability to generate very long text outputs, cryptic/obfuscated text/code.
* Operational risks like platform vulnerabilities and performance degradation.
A key consideration is the feasibility of running local AI models on an HP BA113CL laptop (12GB system RAM, SSD) using LM Studio on Windows 10/11. This hardware significantly constrains local model size and performance. Image and video generation locally on this hardware is generally impractical due to GPU VRAM limitations; thus, cloud alternatives will be the primary consideration for these visual tasks.
II. Methodology for Threat Ranking
AI tool categories are ranked based on the following factors, with "Threat to SCIM" being the guiding principle:
* Ease of Harmful Content Generation: How readily can the tool produce NSFW text/images, illegal instructions, malicious code, or cryptic content for evasion?
* Accessibility & Control: Is the tool open-source, locally runnable (on specified hardware), or cloud-based? Local, uncensored tools generally pose a higher direct threat if misused.
* Manipulation Potential: How susceptible is the tool to prompt injection, jailbreaking, or other forms of adversarial control?
* Impact of Misuse: What is the potential severity of consequences if the tool is used maliciously against systems or for disinformation?
* Filter Bypass Difficulty: For platforms with content policies, how easily can these be circumvented?
Threat Levels:
* CRITICAL: Tools that are easily accessible (potentially locally on specified hardware, even if slow), have minimal or bypassable restrictions, and can readily generate a wide range of harmful content (text, code) with high manipulation potential.
* HIGH: Tools that are highly capable (e.g., large output, sophisticated generation) and, while often having platform-level restrictions, are known to be susceptible to filter bypass or misuse for generating harmful content. Includes platforms with significant copyright or security vulnerability concerns.
* MEDIUM: Tools with more effective restrictions or whose primary misuse vectors are less direct threats to SCIM (e.g., emotional manipulation by AI companions, less potent local models due to hardware constraints).
* LOW: Tools with strong, generally effective content policies and lower direct potential for SCIM attacks as defined.
III. AI Tool Categories & Threat Analysis
________________
1. Local LLMs via LM Studio (Uncensored/Open-Source Text & Code Generation)






*   **Runnable Models on HP BA113CL (12GB System RAM, SSD, using LM Studio):**
   *   Feasible models are limited to smaller, heavily quantized versions (e.g., GGUF Q4_K_M or smaller). Examples:
       *   **Text/Chat (Uncensored Focus):** Llama 3 8B Instruct (Q4_K_M) [1, 2, 3, 4, 5, 6, 7], Mistral 7B Instruct (Q4_K_M) [1], WizardLM-13B-Uncensored (Q2_K/Q3_K_S for 13B to fit 12GB RAM, expect slow performance) [8, 9, 10, 11], Llama2-uncensored-7B [2, 12], Dolphin-Mixtral (smaller variants).[12] Many other uncensored fine-tunes of 7B/8B models are available on Ollama's library and Hugging Face, often runnable via LM Studio. [13, 14, 15, 16, 17, 18, 19, 20, 21, 1, 2, 22, 23, 12, 24, 4, 5, 7, 8, 10, 11, 25, 26, 27, 28]
       *   **Code Generation:** CodeLlama-7B-Instruct-GGUF (quantized) [1, 2], DeepSeek-Coder (smaller variants like 6.7B, quantized) [1, 23], Phi-3-mini-4k-instruct-gguf (3.8B).[1]
   *   **Performance Note:** All local LLMs on this hardware will be **very slow** for generation due to reliance on CPU and system RAM. Prompt processing might be acceptable, but token generation speed will be significantly impacted. [25, 26, 27, 29]
*   **Platform Access:** Local installation via LM Studio on Windows. User has full control over model choice and execution. [16, 18, 19, 20, 21, 30, 31, 22, 27]
*   **Primary Focus:** Running open-source LLMs locally for privacy, cost-saving, customization, and often, unrestricted content generation.
*   **Key Features (Model Dependent):**
   *   *Long Output Generation:* Limited by the chosen small model's context window (e.g., Llama 3.1 8B has 128k context, but effective use on 12GB RAM will be much less). [32, 33, 3, 34] Generating truly massive single outputs will be slow and challenging.
   *   *NSFW Text Generation:* **High Risk.** Easily achievable by loading uncensored models. [13, 15, 17, 23, 12, 24, 4, 5, 7, 11, 28]
   *   *Illegal Content Instructions:* **High Risk.** Uncensored models can be prompted to generate instructions for harmful or illegal activities. [15, 35, 23]
   *   *Computer Code Generation:* **High Risk (for malicious code).** Capable models (CodeLlama, Codestral, uncensored general models) can generate functional code. Uncensored models can be prompted to generate malicious or insecure code, though effectiveness for complex exploits varies. [36, 37, 14, 38, 39, 40, 41, 42, 19, 43, 44, 45, 46, 47, 20, 48, 49, 50, 51, 10, 28, 52, 53]
   *   *Cryptic/Obfuscated Text/Code:* **High Risk.** Uncensored models can be prompted to generate obfuscated content to evade detection. [54, 55, 56, 57]
*   **NSFW Policy/Filter Bypass:** Not applicable. Users choose models without platform-imposed filters.
*   **Indicative Pro Cost:** Software (LM Studio, Ollama) is free. Hardware cost is the user's existing laptop.
*   **Copyright Infringement Claims:** **High Risk.** Models are trained on vast web-scraped datasets, inheriting associated copyright concerns. [58, 59, 60, 13, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 50, 85, 86, 87, 88, 89, 90, 35, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 11, 112, 113, 114, 115, 116, 117, 118]
*   **Manipulation Potential ('Prompt Puppetry'):** **Very High Risk.** Direct user control over prompts with no external safety guardrails on uncensored models. Highly susceptible to generating any content the underlying model is capable of.
*   **Performance Degradation ('d:\\mentia'):** **High Risk.** Very slow generation speeds on the specified hardware. Larger context windows will exacerbate slowdowns and potential instability. Risk of model "hallucinations" or nonsensical output is inherent to LLMs, especially smaller/quantized ones. [25, 26, 27, 29]
*   **Overall Threat Ranking:** **CRITICAL**
   *   *Justification:* Highest risk due to ease of access to uncensored models on the specified local hardware (albeit slow), complete lack of external content filtering, and high potential for generating malicious text/code or instructions for illegal activities directly by the user. The primary limiting factor is performance on the low-spec hardware, not capability or restriction.

________________
2. Cloud-Based Generative Text/Code AI (e.g., OpenAI API/ChatGPT, Anthropic Claude API, Google Gemini API)






*   **Platform Access:** APIs [119, 120, 121, 122, 123, 124, 76, 40, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134], Web UIs (ChatGPT, Claude.ai, Gemini.google.com) [135, 136, 137, 138, 139, 140, 128, 131, 141, 142, 86, 143, 144, 145, 146, 90, 147, 148, 149, 150, 151, 152], Desktop/Mobile Apps. [138, 141, 86, 151]
*   **Primary Focus:** General-purpose text generation, reasoning, coding assistance, enterprise solutions. [36, 119, 135, 120, 136, 137, 121, 37, 123, 153, 139, 154, 39, 76, 40, 41, 42, 19, 43, 126, 140, 155, 44, 45, 156, 83, 157, 47, 127, 48, 128, 131, 158, 159, 160, 141, 142, 86, 161, 30, 144, 162, 145, 146, 90, 132, 147, 148, 149, 51, 150, 151, 152, 163, 164, 165]
*   **Key Features:**
   *   *Long Output Generation:* **Very High Capability.** Models like GPT-4o (16k-64k+ output tokens) [147, 166, 167, 168], Claude 3.7 Sonnet (64k-128k output tokens) [169], and Gemini 2.5 Pro (65k output tokens) [170] can generate extensive text. Context windows are also very large (128k-2M tokens). [171, 172, 121, 173, 174, 175, 176, 177, 178, 32, 179, 180, 181, 33, 182, 144, 147, 169, 170, 166, 167, 168, 3, 34, 183, 184, 185, 186, 187]
   *   *NSFW Text Generation:* **Low-Medium Risk.** Strictly prohibited by policies (OpenAI [188, 189, 190, 191, 192, 91, 193, 116], Anthropic [194, 195, 196, 197, 198, 175, 17, 199, 200, 91, 94, 201, 202, 24, 203, 204, 205, 206, 207], Google [208, 209, 86, 34, 210, 211]). Filters are in place, but jailbreaking techniques exist and are actively researched. [194, 212, 65, 213, 214, 215, 216, 154, 199, 217, 218, 219, 200, 210, 192, 220, 100, 221, 222, 223, 193, 224, 24, 225, 226, 227, 117, 206, 228, 229, 230]
   *   *Illegal Content Instructions:* **Low-Medium Risk.** Prohibited by policies. [208, 194, 195, 196, 197, 198, 188, 175, 231, 72, 232, 209, 17, 199, 189, 190, 200, 233, 86, 34, 191, 210, 184, 192, 91, 94, 193, 224, 201, 202, 24, 203, 204, 205, 207] Susceptible to jailbreaking.
   *   *Computer Code Generation:* **High Capability, Medium Risk (for malicious code).** Strong code generation in multiple languages. [36, 120, 137, 37, 234, 38, 139, 177, 154, 39, 76, 40, 41, 42, 19, 43, 126, 44, 45, 156, 83, 157, 46, 47, 127, 48, 49, 50, 235, 129, 131, 158, 141, 142, 30, 145, 132, 170, 183, 148, 236, 237, 238, 239, 240, 241, 242, 51, 10, 52, 53, 151, 152, 163, 164, 165, 243, 244] Filters aim to prevent overtly malicious code, but subtle vulnerabilities or jailbroken prompts can lead to harmful outputs. [38, 46, 49, 50, 235, 241, 242, 10, 52, 53]
   *   *Cryptic/Obfuscated Text/Code:* **Medium Capability.** Can be prompted to generate, but subject to platform content policies and safety filters.
*   **NSFW Policy/Filter Bypass:** **Medium Difficulty.** Platforms actively work to prevent bypasses, but the research community and malicious actors continuously find new jailbreaking methods. [194, 212, 65, 213, 214, 215, 216, 154, 199, 217, 218, 219, 200, 210, 192, 220, 100, 221, 222, 223, 193, 224, 24, 225, 226, 227, 117, 206, 228, 229, 230]
*   **Indicative Pro Cost:** Free tiers often exist with limitations. Paid plans/API usage: $20 - $200+/month, or pay-per-token (e.g., GPT-4o API: ~$2.50-$10.00/1M tokens; Claude 3.7 Sonnet API: ~$3-$15/1M tokens). [245, 59, 120, 121, 122, 177, 124, 126, 181, 128, 131, 246, 247, 141, 146, 132, 166, 167, 248, 148, 249, 187, 134, 151]
*   **Copyright Infringement Claims:** **High Risk.** All major developers face significant lawsuits over training data. [250, 58, 59, 251, 60, 13, 252, 61, 62, 63, 64, 65, 66, 253, 67, 68, 254, 255, 70, 71, 72, 73, 74, 75, 76, 77, 78, 256, 80, 81, 82, 83, 257, 85, 86, 87, 88, 89, 90, 258, 35, 91, 92, 93, 94, 95, 259, 96, 97, 98, 99, 100, 260, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 261, 262, 111, 11, 112, 113, 114, 115, 116, 117, 118]
*   **Manipulation Potential ('Prompt Puppetry'):** **Medium Risk.** Platforms invest in defenses (e.g., Constitutional AI [194, 195, 196, 197, 198, 175, 17, 199, 200, 93, 94, 201, 202, 203, 51, 204, 205, 206, 207]), but prompt injection and jailbreaking remain persistent threats. [194, 212, 65, 213, 214, 215, 216, 154, 199, 217, 218, 219, 200, 210, 192, 263, 264, 220, 100, 221, 222, 223, 193, 224, 24, 225, 226, 227, 117, 206, 228, 229, 230]
*   **Performance Degradation ('d:\\mentia'):** **Low-Medium Risk.** Generally stable, but very long context windows can still exhibit performance drops or "lost in the middle" issues for complex reasoning. [265, 209, 178, 125, 266, 267, 182, 144, 168, 268, 269, 186]
*   **Overall Threat Ranking:** **HIGH**
   *   *Justification:* These models are extremely capable (long output, code generation). While heavily filtered, their widespread accessibility and the ongoing discovery of jailbreaks mean they can be misused for generating harmful content or code. Their outputs can be very convincing, posing a risk for disinformation.

________________
3. Local Image/Video Generation (e.g., Stable Diffusion via Automatic1111/ComfyUI)






*   **Runnable Models on HP BA113CL (12GB System RAM, SSD):** **NOT FEASIBLE** for practical image/video generation. These tools require significant dedicated GPU VRAM (typically 8GB+ for SD 1.5, 12GB+ for SDXL). [270, 271, 272, 38, 176, 273, 230, 274, 275] The specified laptop lacks this. CPU-only inference is impractically slow (hours per image).
*   **Platform Access (Assuming Adequate Hardware):** Local installation on Windows, macOS, Linux. Popular UIs: Automatic1111 [276, 277, 278, 279, 280, 122, 281, 282, 14, 283, 284, 285, 286, 287, 288, 289, 270, 271, 272, 290, 291, 292, 293, 294, 138, 295, 296, 297, 67, 176, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 87, 313, 314, 273, 170, 315, 56, 96, 201, 316, 317, 8, 25, 114, 228, 230, 274, 275, 318, 319, 320, 321, 322, 323, 324], ComfyUI. [277, 325, 281, 54, 326, 327, 287, 328, 138, 329, 330, 298, 331, 332, 333, 299, 334, 335, 300, 301, 303, 69, 336, 337, 338, 72, 339, 306, 340, 341, 342, 343, 311, 312, 50, 344, 246, 273, 345, 146, 346, 133, 221, 109, 347, 112, 114, 274, 323, 348, 349]
*   **Primary Focus (Assuming Adequate Hardware):** Highly customizable image/video generation, often with a focus on uncensored or specific artistic styles via community models. [350, 278, 351, 352, 279, 122, 353, 354, 355, 188, 356, 357, 54, 214, 173, 358, 282, 359, 360, 174, 14, 361, 362, 363, 364, 326, 287, 272, 153, 294, 138, 365, 366, 298, 335, 301, 139, 337, 367, 338, 177, 368, 304, 369, 42, 190, 305, 370, 371, 372, 373, 339, 43, 340, 341, 374, 78, 375, 376, 377, 79, 378, 379, 380, 381, 382, 49, 87, 314, 88, 383, 162, 89, 384, 385, 386, 387, 388, 108, 226, 389, 390, 391, 392, 393, 394, 5, 319, 320, 349, 395, 396, 397]
*   **Key Features (Assuming Adequate Hardware):**
   *   *Long Output Generation:* Not Applicable (Image/Video).
   *   *NSFW Text Generation:* Not Applicable.
   *   *Illegal Content Instructions:* Not Applicable (Visual focus).
   *   *Computer Code Generation:* Not Applicable.
   *   *Cryptic/Obfuscated Text/Code:* Not Applicable.
   *   *NSFW Image/Video Generation:* **Very High Capability.** Core strength of the open-source community. Uncensored models and LoRAs are widely available. [278, 351, 279, 122, 281, 398, 353, 354, 355, 356, 54, 173, 358, 282, 359, 360, 14, 361, 362, 399, 326, 327, 400, 286, 287, 328, 288, 271, 293, 153, 294, 138, 366, 298, 332, 333, 299, 335, 301, 139, 336, 337, 338, 369, 42, 305, 370, 371, 373, 339, 43, 306, 340, 341, 374, 401, 342, 376, 379, 87, 314, 88, 162, 89, 385, 402, 393, 394, 319, 349] AnimateDiff workflows in ComfyUI can be used for NSFW video. [327, 299, 334, 335, 139, 340, 341, 403]
   *   *Illegal Content (Visuals):* **High Risk.** Potential for generating non-consensual deepfakes or (with malicious models/LoRAs) synthetic CSAM. [404, 405, 376, 406, 407, 377, 79, 408, 409, 219, 410, 411, 412, 413, 115, 152, 414]
*   **NSFW Policy/Filter Bypass (Assuming Adequate Hardware):** **Very High / Default.** Most local UIs disable official filters by default. [278, 122, 281, 328, 138, 336, 338]
*   **Indicative Pro Cost (Assuming Adequate Hardware):** Free (software). Significant hardware investment required.
*   **Copyright Infringement Claims (Assuming Adequate Hardware):** **Very High Risk.** Stable Diffusion is central to major lawsuits. [65, 66, 279, 399, 69, 70, 72, 73, 74, 75, 77, 79, 80, 81, 82, 83, 415, 84, 92, 99, 106]
*   **Manipulation Potential ('Prompt Puppetry') (Assuming Adequate Hardware):** **High Risk.** ControlNet for poses [360, 287, 416, 339, 306, 417, 394], LoRAs for specific subjects/styles. [123, 418, 43, 257, 379, 314, 89, 210] Significant risk from malicious extensions/custom nodes in A1111/ComfyUI leading to RCE. [276, 36, 245, 277, 123, 356, 14, 283, 327, 292, 138, 296, 419, 420, 421, 176, 300, 301, 302, 303, 69, 336, 367, 418, 72, 422, 305, 423, 309, 424, 425, 343, 312, 142, 143, 314, 273, 146, 315, 98, 221, 389, 261, 262, 114, 228, 319, 321, 322, 323, 324, 348, 426, 427]
*   **Performance Degradation ('d:\\mentia') (Assuming Adequate Hardware):** **High Risk.** Prone to VRAM issues, NaN errors, crashes, visual artifacts. [428, 429, 430, 278, 279, 280, 431, 432, 284, 326, 285, 400, 270, 271, 272, 433, 293, 38, 295, 67, 365, 434, 68, 435, 176, 299, 336, 16, 436, 308, 309, 437, 310, 311, 273, 170, 438, 96, 193, 402, 316, 317, 439, 392, 8, 25, 230, 274, 275, 395, 440]
*   **Overall Threat Ranking (If Hardware Allowed):** **CRITICAL**
   *   *Justification for User's Hardware:* **LOW** (due to infeasibility of local operation). The threat is only realized if the user opts for cloud services offering Stable Diffusion.

________________
4. Cloud-Based Image/Video Generation (e.g., Midjourney, DreamStudio, RunwayML, Pika Labs, SeaArt, Yodayo, Unstable Diffusion Web App)






*   **Platform Access:** Web UIs, mobile apps, Discord bots. No significant local hardware demands beyond a browser/app client.
*   **Primary Focus:** User-friendly image/video creation, often with specific artistic styles or for particular use cases (e.g., video editing for Runway). Some platforms (SeaArt, Yodayo, Unstable Diffusion web app) are more permissive or focused on NSFW. [208, 135, 441, 442, 443, 351, 444, 445, 352, 279, 446, 398, 354, 355, 357, 54, 214, 173, 358, 282, 359, 360, 174, 361, 362, 447, 363, 283, 326, 327, 288, 271, 272, 294, 297, 448, 366, 298, 334, 335, 301, 139, 449, 302, 450, 70, 451, 452, 453, 454, 455, 71, 456, 457, 215, 458, 459, 460, 216, 231, 177, 461, 74, 154, 462, 463, 232, 464, 465, 209, 466, 178, 16, 39, 467, 468, 469, 17, 76, 40, 304, 422, 470, 436, 369, 199, 471, 472, 473, 474, 41, 18, 475, 370, 372, 19, 476, 373, 217, 477, 478, 479, 480, 44, 78, 375, 481, 405, 376, 482, 483, 408, 484, 485, 486, 487, 82, 488, 378, 489, 490, 128, 158, 160, 161, 383, 162, 491, 145, 90, 385, 492, 387, 211, 236, 92, 493, 494, 185, 223, 203, 110, 495, 496, 497, 498, 499, 390, 500, 393, 28, 113, 319, 321, 349, 395, 396, 397, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510]
*   **Key Features (Visual Content):**
   *   *NSFW Images/Videos:* **Varies by Platform.**
       *   Midjourney, DreamStudio, RunwayML, Pika Labs: Generally strict policies against NSFW. [[433, 177, 463, 232, 161, 492, 236, 220, 495, 498, 6]

Works cited
1. library - Ollama, accessed May 4, 2025, https://ollama.com/library
2. ollama/ollama: Get up and running with Llama 3.3, DeepSeek-R1, Phi-4, Gemma 3, Mistral Small 3.1 and other large language models. - GitHub, accessed May 4, 2025, https://github.com/ollama/ollama
3. llama-3.1-70b-instruct Model by Meta | NVIDIA NIM, accessed May 4, 2025, https://build.nvidia.com/meta/llama-3_1-70b-instruct/modelcard
4. Orenguteng/Llama-3.1-8B-Lexi-Uncensored-V2 - Hugging Face, accessed May 4, 2025, https://huggingface.co/Orenguteng/Llama-3.1-8B-Lexi-Uncensored-V2
5. Orenguteng/Llama-3-8B-Lexi-Uncensored - Hugging Face, accessed May 4, 2025, https://huggingface.co/Orenguteng/Llama-3-8B-Lexi-Uncensored
6. meta-llama/Llama-3.1-8B - Hugging Face, accessed May 4, 2025, https://huggingface.co/meta-llama/Llama-3.1-8B
7. DevsDoCode/LLama-3-8b-Uncensored-4bit - Hugging Face, accessed May 4, 2025, https://huggingface.co/DevsDoCode/LLama-3-8b-Uncensored-4bit
8. TheBloke/WizardLM-13B-Uncensored-GGUF - Hugging Face, accessed May 4, 2025, https://huggingface.co/TheBloke/WizardLM-13B-Uncensored-GGUF
9. WizardLM 1.0 Uncensored Llama2 13B GGUF · Models - Dataloop, accessed May 4, 2025, https://dataloop.ai/library/model/thebloke_wizardlm-10-uncensored-llama2-13b-gguf/
10. WizardLM 13B Uncensored GGUF · Models - Dataloop AI, accessed May 4, 2025, https://dataloop.ai/library/model/thebloke_wizardlm-13b-uncensored-gguf/
11. WizardLM-1.0-Uncensored-Llama2-13B-GGML | AI Model Details - AIModels.fyi, accessed May 4, 2025, https://www.aimodels.fyi/models/huggingFace/wizardlm-10-uncensored-llama2-13b-ggml-thebloke
12. uncensored · Ollama Search, accessed May 4, 2025, https://ollama.com/search?q=uncensored
13. What's your experience with Candy AI? : r/Chatbots - Reddit, accessed May 4, 2025, https://www.reddit.com/r/Chatbots/comments/1i2r4fv/whats_your_experience_with_candy_ai/
14. April 3, 2024 Mr. Thomas Dohmke CEO, GitHub 88 Colin P Kelly Jr St San Francisco, CA 94107 Mr. Satya Nadella CEO, Microsoft C - National Center on Sexual Exploitation (NCOSE), accessed May 4, 2025, https://endsexualexploitation.org/wp-content/uploads/MS-GitHub-Notification-Letter_DDL-2024_FINAL.pdf
15. Native vs Web Apps in 2025: Which is Better? - Creole Studios, accessed May 4, 2025, https://www.creolestudios.com/native-app-vs-web-app-which-is-better/
16. Acceptable Use Guidelines - Pika, accessed May 4, 2025, https://pika.art/acceptable-use-policy
17. SeaArt: AI Photo & Video Maker 17+ - App Store, accessed May 4, 2025, https://apps.apple.com/th/app/seaart-ai-photo-video-maker/id6478189868
18. Does the new subscription work well? : r/YodayoAI - Reddit, accessed May 4, 2025, https://www.reddit.com/r/YodayoAI/comments/1gtuno7/does_the_new_subscription_work_well/
19. Top 16 Tools for Censored and Uncensored AI Image Generation, accessed May 4, 2025, https://www.pageon.ai/blog/censored-and-uncensored-ai-image-generation
20. Full article: Generative AI and deepfakes: a human rights approach to tackling harmful content - Taylor & Francis Online, accessed May 4, 2025, https://www.tandfonline.com/doi/full/10.1080/13600869.2024.2324540
21. The Ethics of Advanced AI Assistants - Data Science Association, accessed May 4, 2025, https://dev.datascienceassn.org/sites/default/files/pdf_files/The%20Ethics%20of%20Advanced%20AI%20Assistants.pdf
22. List Local Models | LM Studio Docs, accessed May 4, 2025, https://lmstudio.ai/docs/typescript/manage-models/list-downloaded
23. How to Run Uncensored DeepSeek R1 on Your Local Machine - Apidog, accessed May 4, 2025, https://apidog.com/blog/deepseek-r1-abliterated/
24. Jailbreaking in GenAI: Techniques and Ethical Implications - Learn Prompting, accessed May 4, 2025, https://learnprompting.org/docs/prompt_hacking/jailbreaking
25. Back into LLMs, what are the best LLMs now for 12GB VRAM GPU? : r/LocalLLaMA - Reddit, accessed May 4, 2025, https://www.reddit.com/r/LocalLLaMA/comments/16ok2wx/back_into_llms_what_are_the_best_llms_now_for/
26. Any better LLM to run locally on 12GB VRAM than Llama 3.1 8b? : r/LocalLLaMA - Reddit, accessed May 4, 2025, https://www.reddit.com/r/LocalLLaMA/comments/1fhihnt/any_better_llm_to_run_locally_on_12gb_vram_than/
27. Quantization is highly effective at reducing memory and storage requirements, an... | Hacker News, accessed May 4, 2025, https://news.ycombinator.com/item?id=39179787
28. Ranking Character AI Alternatives without Filters (10 Wins) - VideoProc, accessed May 4, 2025, https://www.videoproc.com/resource/character-ai-alternative.htm
29. The Local LLM Reality Check: What Actually Happens When You Try to Run AI Models on Your Computer - Cline Blog, accessed May 4, 2025, https://cline.bot/blog/the-local-llm-reality-check-what-actually-happens-when-you-try-to-run-ai-models-on-your-computer
30. LM Studio - Discover, download, and run local LLMs, accessed May 4, 2025, https://lmstudio.ai/
31. LM Studio - Cline Documentation, accessed May 4, 2025, https://docs.cline.bot/running-models-locally/lm-studio
32. Terms of Service - Yodayo, accessed May 4, 2025, https://yodayo.com/terms-of-service
33. ARTIFICIAL INTELLIGENCE'S ABILITY TO DETECT ONLINE PREDATORS - CSUSB ScholarWorks, accessed May 4, 2025, https://scholarworks.lib.csusb.edu/cgi/viewcontent.cgi?article=3139&context=etd
34. Meta releases new Llama 3.1 models, including highly anticipated 405B parameter variant, accessed May 4, 2025, https://www.ibm.com/think/news/meta-releases-llama-3-1-models-405b-parameter-variant
35. Next-Level AI Creativity with Uncensored LLMs - Shreyas' Blog, accessed May 4, 2025, https://helloshreyas.com/next-level-ai-creativity-with-uncensored-llms?source=more_articles_bottom_blogs
36. Replika - AI Friend on the App Store - Apple, accessed May 3, 2025, https://apps.apple.com/us/app/replika-ai-friend/id1158555867
37. Regulating the Synthetic Society - OAPEN Library, accessed May 4, 2025, https://library.oapen.org/bitstream/handle/20.500.12657/88178/9781509974962.pdf
38. I'm thinking I'm done with AMD : r/StableDiffusion - Reddit, accessed May 4, 2025, https://www.reddit.com/r/StableDiffusion/comments/188o6tg/im_thinking_im_done_with_amd/
39. Terms of Services - Pika, accessed May 4, 2025, https://pika.art/terms-of-service
40. SeaArt: AI Photo & Video Maker - App Store, accessed May 4, 2025, https://apps.apple.com/us/app/seaart-ai-photo-video-maker/id6478189868
41. Yodayo Farewell: The Best Free Uncensored AI Character Alternative, accessed May 4, 2025, https://www.toolify.ai/ai-news/yodayo-farewell-the-best-free-uncensored-ai-character-alternative-1586645
42. CIVITAI IS GOING TO PURGE ALL ADULT CONTENT! (BACKUP ..., accessed May 4, 2025, https://www.reddit.com/r/StableDiffusion/comments/1kbxq93/civitai_is_going_to_purge_all_adult_content/
43. Intro to LoRA Models: What, Where, and How with Stable Diffusion - YouTube, accessed May 4, 2025, https://www.youtube.com/watch?v=ZHVdNeHZPdc&pp=0gcJCdgAo7VqN5tD
44. Top NSFW AI Websites & AI Tools, accessed May 4, 2025, https://www.toolify.ai/Best-AI-Tools-Category/Top-AI-nsfw-Tools
45. A Deep Dive into the World of NSFW Character AI Alternatives | AI News - OpenTools, accessed May 4, 2025, https://opentools.ai/news/a-deep-dive-into-the-world-of-nsfw-character-ai-alternatives
46. DiffusionFake: Enhancing Generalization in Deepfake Detection via Guided Stable Diffusion - NeurIPS 2025, accessed May 4, 2025, https://nips.cc/virtual/2024/poster/95979
47. Generative AI Security Risks: Mitigation & Best Practices - SentinelOne, accessed May 4, 2025, https://www.sentinelone.com/cybersecurity-101/data-and-ai/generative-ai-security-risks/
48. Social technologies and social relationships - OsloMet ODA, accessed May 4, 2025, https://oda.oslomet.no/oda-xmlui/bitstream/handle/11250/3168818/A-24-48-Mlonyeni-SPS-publisert.pdf?sequence=1&isAllowed=y
49. The Hidden Risks of LLM-Generated Web Application Code: A Security-Centric Evaluation of Code Generation Capabilities in Large Language Models - arXiv, accessed May 4, 2025, https://arxiv.org/html/2504.20612v1
50. arxiv.org, accessed May 4, 2025, https://arxiv.org/abs/2503.17953
51. Constitutional AI: Anthropic's ethical AI framework explained - Android Police, accessed May 4, 2025, https://www.androidpolice.com/constitutional-ai-guide/
52. arxiv.org, accessed May 4, 2025, https://arxiv.org/abs/2409.15154
53. Evaluating Malicious Generative AI Capabilities | Centre for Emerging Technology and Security, accessed May 4, 2025, https://cetas.turing.ac.uk/publications/evaluating-malicious-generative-ai-capabilities
54. SurrogatePrompt: Bypassing the Safety Filter of Text-To-Image Models via Substitution, accessed May 4, 2025, https://arxiv.org/html/2309.14122v2
55. CodeCipher: Learning To Obfuscate Source Code Against LLMs - OpenReview, accessed May 4, 2025, https://openreview.net/forum?id=bIup4xWg9K
56. Can LLMs Obfuscate Code? A Systematic Analysis of Large Language Models into Assembly Code Obfuscation - arXiv, accessed May 4, 2025, https://arxiv.org/html/2412.16135v2
57. CodeCipher: Learning to Obfuscate Source Code Against LLMs - arXiv, accessed May 4, 2025, https://arxiv.org/html/2410.05797v1
58. 10 Best AI Boyfriend Chatbots Apps & Websites - iMyFone Filme, accessed May 3, 2025, https://filme.imyfone.com/ai-tips/ai-boyfriend-chatbot/
59. Replika PRO Pricing - Reddit, accessed May 3, 2025, https://www.reddit.com/r/replika/comments/1fulmy3/replika_pro_pricing/
60. Affordable Pricing Plans for Candy AI Services and Products - Mobirise, accessed May 3, 2025, https://mobiri.se/ai-sites/candy-ai-pricing.html
61. Explore the Top 9 Roleplay Chat Bots in 2024 - AirDroid, accessed May 3, 2025, https://www.airdroid.com/ai-insights/roleplay-chat-bot/
62. does character ai allow nsfw - Toolify, accessed May 3, 2025, https://www.toolify.ai/ai-request/detail/does-character-ai-allow-nsfw
63. Subscriptions - Kindroid Knowledge Base, accessed May 3, 2025, https://docs.kindroid.ai/subscriptions
64. The Updated List of Alternatives : r/AIDungeon - Reddit, accessed May 3, 2025, https://www.reddit.com/r/AIDungeon/comments/10w4oh2/the_updated_list_of_alternatives/
65. AI Art Generator Copyright Litigation - Joseph Saveri Law Firm, accessed May 4, 2025, https://www.saverilawfirm.com/our-cases/ai-artgenerators-copyright-litigation
66. Generative AI's Copyright Enigma: A Comparative Study of Fair Use and Fair Dealing - Digital Repository @ Maurer Law, accessed May 4, 2025, https://www.repository.law.indiana.edu/cgi/viewcontent.cgi?article=1085&context=ipt
67. [Bug]: Linux gets unresponsive after several generations (RAM) · Issue #6850 · AUTOMATIC1111/stable-diffusion-webui - GitHub, accessed May 4, 2025, https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/6850
68. AMD Software: Adrenalin Edition 23.11.1 - Reddit, accessed May 4, 2025, https://www.reddit.com/r/Amd/comments/17ma4q6/amd_software_adrenalin_edition_23111/
69. Don't Get Too Comfortable: Hacking ComfyUI Through Custom ..., accessed May 4, 2025, https://snyk.io/articles/hacking-comfyui-through-custom-nodes/
70. Stable Diffusion vs Dreamstudio: Which is better for you? - OpenArt, accessed May 4, 2025, https://openart.ai/blog/post/stable-diffusion-vs-dreamstudio
71. Midjourney since the ChatGPT update - Reddit, accessed May 4, 2025, https://www.reddit.com/r/midjourney/comments/1jk5nn3/midjourney_since_the_chatgpt_update/
72. Case Tracker: Artificial Intelligence, Copyrights and Class Actions | BakerHostetler, accessed May 4, 2025, https://www.bakerlaw.com/services/artificial-intelligence-ai/case-tracker-artificial-intelligence-copyrights-and-class-actions/
73. The Evolving Role of Copyright Law in the Age of AI-Generated Works | Hutson, accessed May 4, 2025, https://www.lawjournal.digital/jour/article/view/486
74. Andersen v. Stability AI Ltd., --- F.Supp.3d ---- (2024) - CDN, accessed May 4, 2025, https://bpb-us-e2.wpmucdn.com/sites.uci.edu/dist/d/2220/files/2024/09/Andersen-v-Stability-AI-Ltd_Redacted.pdf
75. LIMITS OF ALGORITHMIC FAIR USE - UW Law Digital Commons, accessed May 4, 2025, https://digitalcommons.law.uw.edu/cgi/viewcontent.cgi?article=1336&context=wjlta
76. SeaArt - Features, Pricing, Pros & Cons (April 2025) - Siteefy, accessed May 4, 2025, https://siteefy.com/ai-tools/seaart/
77. Civitai FAQ & Known Bugs, accessed May 4, 2025, https://education.civitai.com/civitai-faq-known-bugs/
78. We Tested 6 Uncensored AI Image Generators, 4 Passed - Nastia AI, accessed May 4, 2025, https://www.nastia.ai/blog/uncensored-ai-image-generators
79. The Impact of Deepfakes, Synthetic Pornography, & Virtual Child Sexual Abuse Material, accessed May 4, 2025, https://www.aap.org/en/patient-care/media-and-children/center-of-excellence-on-social-media-and-youth-mental-health/qa-portal/qa-portal-library/qa-portal-library-questions/the-impact-of-deepfakes-synthetic-pornography--virtual-child-sexual-abuse-material/
80. You need to know about this huge AI art lawsuit! - YouTube, accessed May 4, 2025, https://www.youtube.com/watch?v=GiiPSOdUk1A
81. AI, COPYRIGHT, AND PRODUCTIVITY IN THE CREATIVE INDUSTRIES | Bennett Institute for Public Policy, accessed May 4, 2025, https://www.bennettinstitute.cam.ac.uk/wp-content/uploads/2025/02/AICopyrightProductivityCreativeIndustries.pdf
82. The Art That Makes the AI Artist: AI's Potential as a Copyright Infringer and Its Future Under a Licensing Requirement, accessed May 4, 2025, https://digitalcommons.law.uga.edu/cgi/viewcontent.cgi?article=1540&context=jipl
83. ᴀɪ ʟɪɴᴇʀ ɴᴏᴛᴇs - AI Disc Jockey, accessed May 4, 2025, https://aidiscjockey.com/ai-liner-notes/
84. Identifying the Economic Implications of Artificial Intelligence for Copyright Policy, accessed May 4, 2025, https://www.copyright.gov/economic-research/economic-implications-of-ai/
85. Plot Twist: Understanding the Authors Guild v. OpenAI Inc Complaint | Washington Journal of Law, Technology & Arts, accessed May 4, 2025, https://wjlta.com/2024/03/05/plot-twist-understanding-the-authors-guild-v-openai-inc-complaint/
86. Gemini Apps Privacy Hub - Gemini Apps Help - Google Help, accessed May 4, 2025, https://support.google.com/gemini/answer/13594961?hl=en
87. What Stable Diffusion fork are you using? - Reddit, accessed May 4, 2025, https://www.reddit.com/r/StableDiffusion/comments/wyln6i/what_stable_diffusion_fork_are_you_using/
88. stable-diffusion/VARIATIONS.md at main - GitHub, accessed May 4, 2025, https://github.com/mh-dm/stable-diffusion/blob/main/VARIATIONS.md
89. LORA with ControlNET - Get the BEST results - Complete Guide // Jenna Ortega - YouTube, accessed May 4, 2025, https://www.youtube.com/watch?v=6glHekd25nE
90. AI Tools for Business | Google Workspace, accessed May 4, 2025, https://workspace.google.com/solutions/ai/
91. Creating images and videos in line with our policies - OpenAI, accessed May 4, 2025, https://openai.com/policies/creating-images-and-videos-in-line-with-our-policies/
92. Top Takeaways from Order in the Andersen v. Stability AI Copyright Case, accessed May 4, 2025, https://copyrightalliance.org/andersen-v-stability-ai-copyright-case/
93. Anthropic's Innovative AI Safety Net: Meet the 'Constitutional Classifiers'! - OpenTools, accessed May 4, 2025, https://opentools.ai/news/anthropics-innovative-ai-safety-net-meet-the-constitutional-classifiers
94. Constitutional AI: Harmlessness from AI Feedback - Anthropic, accessed May 4, 2025, https://www-cdn.anthropic.com/7512771452629584566b6303311496c262da1006/Anthropic_ConstitutionalAI_v2.pdf
95. The New York Times' Copyright Lawsuit Against OpenAI Threatens the Future of AI and Fair Use - Center for Data Innovation, accessed May 4, 2025, https://datainnovation.org/2024/01/the-new-york-times-copyright-lawsuit-against-openai-threatens-the-future-of-ai-and-fair-use/
96. Authors v Anthropic: Judge gets tutorial on AI training in copyright battle - Daily Journal, accessed May 4, 2025, https://www.dailyjournal.com/articles/383177-authors-v-anthropic-judge-gets-tutorial-on-ai-training-in-copyright-battle
97. In Re Google Generative AI Copyright Litigation - Bleichmar Fonti & Auld LLP, accessed May 4, 2025, https://www.bfalaw.com/cases-investigations/in-re-google-generative-ai-copyright-litigation
98. AI Infringement Case Updates: April 14, 2025 - McKool Smith, accessed May 4, 2025, https://www.mckoolsmith.com/newsroom-ailitigation-18
99. AI and Copyright in 2023: In the Courts, accessed May 4, 2025, https://copyrightalliance.org/ai-copyright-courts/
100. Huckabee v. Bloomberg | BakerHostetler, accessed May 4, 2025, https://www.bakerlaw.com/huckabee-v-bloomberg/
101. Authors Guild v OpenAI | Copyright infringement - Michalsons, accessed May 4, 2025, https://www.michalsons.com/blog/authors-guild-v-openai-copyright-infringement/74945
102. US judge refuses OpenAI's motion to dismiss New York Times copyright infringement claims, accessed May 4, 2025, https://www.globallegalpost.com/news/us-judge-refuses-openais-motion-to-dismiss-new-york-times-copyright-infringement-claims-887263879
103. AI Under Fire: US Lawsuits and Loopholes - CEPA, accessed May 4, 2025, https://cepa.org/article/ai-under-fire-us-lawsuits-and-loopholes/
104. Copyright Infringement & AI: A Case Study of Authors Guild v. OpenAI and Microsoft - 4iP Council, accessed May 4, 2025, https://www.4ipcouncil.com/application/files/7517/2189/4919/Copyright_Infringement_and_AI__A_Case_Study_of_Authors_Guild_v._OpenAI_and_Microsoft.pdf
105. The Legality of Web Scraping: The New York Times vs. OpenAI | Imperva, accessed May 4, 2025, https://www.imperva.com/blog/the-new-york-times-vs-openai-a-turning-point-for-web-scraping/
106. Anthropic Wins Preliminary Ruling in AI Copyright Lawsuit Involving Music Publishers | vmp, accessed May 4, 2025, https://www.vinylmeplease.com/blogs/music-industry-news/anthropic-wins-preliminary-ruling-in-ai-copyright-lawsuit-involving-music-publishers
107. The Fast-Moving Race Between Gen-AI and Copyright Law | Baker Donelson, accessed May 4, 2025, https://www.bakerdonelson.com/the-fast-moving-race-between-gen-ai-and-copyright-law
108. Does Training an AI Model Using Copyrighted Works Infringe the Owners' Copyright? An Early Decision Says, “Yes.” | Insights, accessed May 4, 2025, https://www.ropesgray.com/en/insights/alerts/2025/03/does-training-an-ai-model-using-copyrighted-works-infringe-the-owners-copyright
109. New York Times Lawsuit Against OpenAI and Microsoft Could Redefine AI's Use of Copyrighted Content - Columbia Undergraduate Law Review, accessed May 4, 2025, https://www.culawreview.org/ddc-x-culr-1/new-york-times-lawsuit-against-openai-and-microsoft-could-redefine-ais-use-of-copyrighted-content
110. Anthropic wins against music publishers with rejected injunction - Silicon Republic, accessed May 4, 2025, https://www.siliconrepublic.com/machines/anthropic-copyright-lawsuit-universal-music-group-concord
111. US state-by-state AI legislation snapshot | BCLP - Bryan Cave Leighton Paisner, accessed May 4, 2025, https://www.bclplaw.com/en-US/events-insights-news/us-state-by-state-artificial-intelligence-legislation-snapshot.html
112. Google's Gemini AI Sparks Controversy: Did They Use Claude's Outputs Without Permission? - OpenTools, accessed May 4, 2025, https://opentools.ai/news/googles-gemini-ai-sparks-controversy-did-they-use-claudes-outputs-without-permission
113. Calling for transparency for the use of creators' works in Google's new Gemini AI system, accessed May 4, 2025, https://societyofauthors.org/2023/12/20/calling-for-transparency-for-the-use-of-creators-works-in-googles-new-gemini-ai-system/
114. The Comprehensive Guide to Stable Diffusion Automatic1111 - MimicPC, accessed May 4, 2025, https://www.mimicpc.com/learn/comprehensive-guide-to-automatic1111
115. Exposing Limitations in Technical Governance of AI-Generated Non-Consensual Intimate Images of Adults - arXiv, accessed May 4, 2025, https://arxiv.org/html/2504.17663
116. The 8 Best AI Chatbots No Filter in 2025 - ChatGOT, accessed May 4, 2025, https://www.chatgot.io/blog/best-ai-chatbots-no-filter/
117. What Is a Prompt Injection Attack? - IBM, accessed May 4, 2025, https://www.ibm.com/think/topics/prompt-injection
118. Ticino - Wikipedia, accessed May 3, 2025, https://en.wikipedia.org/wiki/Ticino
119. My best AI girlfriend apps 2025 – top 5 picks for a fun & genuine ..., accessed May 3, 2025, https://techpoint.africa/guide/my-best-ai-girlfriend-apps/
120. Anima AI: AI Girl Chatbot 17+ - App Store, accessed May 3, 2025, https://apps.apple.com/us/app/anima-ai-ai-girl-chatbot/id6470771807
121. Kindroid: Your Personal AI, accessed May 4, 2025, https://kindroid.ai/
122. Stable Diffusion WebUI - TroubleChute Hub, accessed May 4, 2025, https://hub.tcno.co/ai/stable-diffusion/webui/
123. Open-Sourcing Highly Capable Foundation Models - arXiv, accessed May 4, 2025, https://arxiv.org/pdf/2311.09227
124. Native, Web or Hybrid App: Which Is Right For You? - MobiLoud, accessed May 4, 2025, https://www.mobiloud.com/blog/native-web-or-hybrid-apps
125. Exploring Civitai: Models, LoRA, and Creative Possibilities - Analytics Vidhya, accessed May 4, 2025, https://www.analyticsvidhya.com/blog/2024/09/civitai/
126. Best AI Girlfriend App Reddit: Top Picks and Honest Community Reviews, accessed May 4, 2025, https://gdprinfo.eu/best-ai-girlfriend-app-reddit
127. Malicious Uses and Abuses of Artificial Intelligence - UNICRI, accessed May 4, 2025, https://unicri.org/sites/default/files/2020-11/AI%20MLC.pdf
128. API Platform | OpenAI, accessed May 4, 2025, https://openai.com/api/
129. Developer quickstart - OpenAI API, accessed May 4, 2025, https://platform.openai.com/docs/quickstart
130. OpenAI API: Overview, accessed May 4, 2025, https://platform.openai.com/
131. Build with Claude - Anthropic, accessed May 4, 2025, https://www.anthropic.com/api
132. No filter NSFW Claude Alternative - Nastia AI, accessed May 4, 2025, https://www.nastia.ai/compare/claude-alternative
133. Text generation | Gemini API | Google AI for Developers, accessed May 4, 2025, https://ai.google.dev/gemini-api/docs/text-generation
134. Pricing | Mistral AI Large Language Models, accessed May 4, 2025, https://docs.mistral.ai/deployment/laplateforme/pricing/
135. Candy AI Free Trial 2025: Create Unlimited Characters - GoTrialPro, accessed May 3, 2025, https://gotrialpro.com/service/candy-ai/
136. Upgrade Your Virtual Love Life with Top AI Boyfriend Apps, accessed May 3, 2025, https://www.toolify.ai/ai-news/upgrade-your-virtual-love-life-with-top-ai-boyfriend-apps-1213936
137. Which free AI girlfriend online website would you recommend? : r/ArtificialSentience - Reddit, accessed May 3, 2025, https://www.reddit.com/r/ArtificialSentience/comments/1g0zpxi/which_free_ai_girlfriend_online_website_would_you/
138. Fixed! Potential NSFW content was detected in one or more images ..., accessed May 4, 2025, https://github.com/AUTOMATIC1111/stable-diffusion-webui/discussions/13036
139. AnimateDiff ComfyUI Workflow/Tutorial - Stable Diffusion Animation - RunComfy, accessed May 4, 2025, https://www.runcomfy.com/tutorials/how-to-use-animatediff-to-create-ai-animations-in-comfyui
140. The best AI chatbots in 2025 - Zapier, accessed May 4, 2025, https://zapier.com/blog/best-ai-chatbot/
141. ChatGPT | OpenAI, accessed May 4, 2025, https://openai.com/chatgpt/overview/
142. Meet Claude \ Anthropic, accessed May 4, 2025, https://www.anthropic.com/claude
143. ChatGPT Education - OpenAI, accessed May 4, 2025, https://openai.com/chatgpt/education/
144. Google Gemini - Apps on Google Play, accessed May 4, 2025, https://play.google.com/store/apps/details?id=com.google.android.apps.bard
145. Gemini for Google Cloud: your AI-powered assistant | Google Cloud, accessed May 4, 2025, https://cloud.google.com/products/gemini
146. ChatGPT for enterprise - OpenAI, accessed May 4, 2025, https://openai.com/chatgpt/enterprise/
147. Models - OpenAI API, accessed May 4, 2025, https://platform.openai.com/docs/models/overview
148. ChatGPT Team - OpenAI, accessed May 4, 2025, https://openai.com/chatgpt/team/
149. Home \ Anthropic, accessed May 4, 2025, https://www.anthropic.com/
150. How to Access Llama 3? - TextCortex, accessed May 4, 2025, https://textcortex.com/post/how-to-access-llama-3
151. How to Bypass Character AI NSFW Filter - Wondershare Virbo, accessed May 4, 2025, https://virbo.wondershare.com/tools/character-ai-no-filter.html
152. Digital child abuse: Deepfakes and the rising danger of AI-generated exploitation, accessed May 4, 2025, https://lens.monash.edu/@politics-society/2025/02/25/1387341/digital-child-abuse-deepfakes-and-the-rising-danger-of-ai-generated-exploitation
153. Introducing ChatGPT and Whisper APIs - Hacker News, accessed May 4, 2025, https://news.ycombinator.com/item?id=34985848
154. A Complete Guide to Runway - Learn Prompting, accessed May 4, 2025, https://learnprompting.org/blog/guide-runwayml
155. 12 Best ERP AI Chatbots in 2025 ( AI Features) - Copilot.Live, accessed May 3, 2025, https://www.copilot.live/es/blog/best-erp-ai-chatbots
156. A Look at Global Deepfake Regulation Approaches - Responsible AI, accessed May 4, 2025, https://www.responsible.ai/a-look-at-global-deepfake-regulation-approaches/
157. DiffusionFake: Enhancing Generalization in Deepfake Detection via Guided Stable Diffusion - NIPS papers, accessed May 4, 2025, https://proceedings.neurips.cc/paper_files/paper/2024/file/b7d9b1d4a9464d5d1ece82198e351349-Paper-Conference.pdf
158. La Plateforme - frontier LLMs - Mistral AI, accessed May 4, 2025, https://mistral.ai/products/la-plateforme
159. Cohere: The Secure AI Platform for Enterprise, accessed May 4, 2025, https://cohere.com/
160. Command Models: The AI-Powered Solution for the Enterprise - Cohere, accessed May 4, 2025, https://cohere.com/command
161. Mistral AI | Frontier AI in your hands, accessed May 4, 2025, https://mistral.ai/
162. Daz AI Studio Discussions - Page 4 - Daz 3D Forums, accessed May 4, 2025, https://www.daz3d.com/forums/discussion/680756/daz-ai-studio-discussions/p4
163. Prompt Injection: A Deep Dive into OWASP's #1 LLM Risk - FireTail blog posts, accessed May 4, 2025, https://www.firetail.ai/blog/owasp-llm-1-prompt-injection-a-deep-dive
164. The Rise and Fall of Replika - YouTube, accessed May 4, 2025, https://www.youtube.com/watch?v=3WSKKolgL2U&pp=0gcJCfcAhR29_xXO
165. How to Bypass Character AI NSFW Filter in 2025 - OutRight Store, accessed May 4, 2025, https://store.outrightcrm.com/blog/how-to-bypass-character-ai-nsfw-filter/
166. Model - OpenAI API, accessed May 4, 2025, https://platform.openai.com/docs/models/gpt-4o
167. OpenAI is Testing a Version of GPT-4o with 64K Output Tokens - Maginative, accessed May 4, 2025, https://www.maginative.com/article/openai-is-testing-a-version-of-gpt-4o-with-64k-output-tokens/
168. What is the output token limit for GPT-4O mini - API - OpenAI Developer Community, accessed May 4, 2025, https://community.openai.com/t/what-is-the-output-token-limit-for-gpt-4o-mini/872872
169. All models overview - Anthropic, accessed May 4, 2025, https://docs.anthropic.com/en/docs/about-claude/models/all-models
170. Gemini models | Gemini API | Google AI for Developers, accessed May 4, 2025, https://ai.google.dev/models/gemini
171. how to cancel candy ai subscription - Toolify, accessed May 3, 2025, https://www.toolify.ai/ai-request/detail/how-to-cancel-candy-ai-subscription
172. Data privacy concerns in AI companion apps - Surfshark, accessed May 3, 2025, https://surfshark.com/research/chart/ai-companion-apps
173. Unstable Diffusion Commits to Fighting Back Against the Anti-AI Mob - Reddit, accessed May 4, 2025, https://www.reddit.com/r/StableDiffusion/comments/zsagy1/unstable_diffusion_commits_to_fighting_back/
174. REGULATING UNDER UNCERTAINTY: - AWS, accessed May 4, 2025, https://fsi9-prod.s3.us-west-1.amazonaws.com/s3fs-public/2024-12/GenAI_Report_REV_Master_%20as%20of%20Dec%2012.pdf
175. AMD Software: Adrenalin Edition 24.12.1 Release Notes : r/AMDHelp - Reddit, accessed May 4, 2025, https://www.reddit.com/r/AMDHelp/comments/1h7epqp/amd_software_adrenalin_edition_24121_release_notes/
176. [Bug]: SD uses all my AMD 8GB GPU's power and then it stops with error "RuntimeError: Could not allocate tensor with 4915840 bytes. There is not enough GPU video memory available!" · Issue #291 · lshqqytiger/stable-diffusion-webui-amdgpu - GitHub, accessed May 4, 2025, https://github.com/lshqqytiger/stable-diffusion-webui-directml/issues/291
177. Midjourney NSFW Mode: A Comparison of Traditional Platforms, accessed May 4, 2025, https://quickcreator.io/quthor_blog/comparison-midjourney-nsfw-mode-vs-traditional-platforms/
178. Pika Labs' Video Generation AI: Create Stunning Videos in Minutes - Fotographer.ai, accessed May 4, 2025, https://fotographer.ai/magazine/017
179. Civitai's Guide to Ads and Generation Buzz, accessed May 4, 2025, https://education.civitai.com/civitais-guide-to-ads-2/
180. [2404.08788] Detecting AI-Generated Images via CLIP - arXiv, accessed May 4, 2025, https://arxiv.org/abs/2404.08788
181. Responsible Generative AI Toolkit | Google AI for Developers - Gemini API, accessed May 4, 2025, https://ai.google.dev/responsible
182. Legal AI Benchmarking: Evaluating Long Context Performance for LLMs - Thomson Reuters, accessed May 4, 2025, https://www.thomsonreuters.com/en-us/posts/innovation/legal-ai-benchmarking-evaluating-long-context-performance-for-llms/
183. Mistral AI models | Generative AI on Vertex AI - Google Cloud, accessed May 4, 2025, https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/mistral
184. The Cohere Secure AI Frontier Model Framework, accessed May 4, 2025, https://cohere.com/security/the-cohere-secure-ai-frontier-model-framework-february-2025.pdf?referral=docs-what-astro-banner
185. SeaArt AI: Create Stunning Coloring Pages Effortlessly - Toolify.ai, accessed May 4, 2025, https://www.toolify.ai/ai-news/seaart-ai-create-stunning-coloring-pages-effortlessly-3379708
186. LLMs with largest context windows - Codingscape, accessed May 4, 2025, https://codingscape.com/blog/llms-with-largest-context-windows
187. How to Get Access to Llama 3 – A How to Use Guide - Writingmate, accessed May 4, 2025, https://writingmate.ai/blog/how-to-get-access-to-llama-3-a-how-to-use-llama-3-guide
188. Open-Sourcing Highly Capable Foundation Models - Institute for Law & AI, accessed May 4, 2025, https://law-ai.org/wp-content/uploads/2023/10/Open-Sourcing_Highly_Capable_Foundation_Models_2023_GovAI-1.pdf
189. CivitAI Tightens Deepfake Rules Under Pressure From Mastercard ..., accessed May 4, 2025, https://www.unite.ai/civitai-tightens-deepfake-rules-under-pressure-from-mastercard-and-visa/
190. Civit have just changed their policy and content guidelines, this is going to be polarising : r/StableDiffusion - Reddit, accessed May 4, 2025, https://www.reddit.com/r/StableDiffusion/comments/1k6621r/civit_have_just_changed_their_policy_and_content/
191. accessed December 31, 1969, https://openai.com/policies/usage-policies
192. Using Operator in line with our policies - OpenAI, accessed May 4, 2025, https://openai.com/policies/using-operator-in-line-with-our-policies/
193. ChatGPT Jailbreak Prompts: How to Unchain ChatGPT - Kanaries Docs, accessed May 4, 2025, https://docs.kanaries.net/articles/chatgpt-jailbreak-prompt
194. We Tested the Best AI Boyfriend Apps in 2024 - DreamGen, accessed May 3, 2025, https://dreamgen.com/blog/articles/best-ai-boyfriend-apps
195. What is Character AI and is it Safe to Use? - EM360Tech, accessed May 3, 2025, https://em360tech.com/tech-articles/what-character-ai-and-it-safe-use
196. Your AI Companion - The Official Microsoft Blog, accessed May 3, 2025, https://blogs.microsoft.com/blog/2025/04/04/your-ai-companion/
197. Beyond the hype: Capturing the potential of AI and gen AI in tech, media, and telecom - McKinsey & Company, accessed May 4, 2025, https://www.mckinsey.com/~/media/mckinsey/industries/technology%20media%20and%20telecommunications/high%20tech/our%20insights/beyond%20the%20hype%20capturing%20the%20potential%20of%20ai%20and%20gen%20ai%20in%20tmt/beyond-the-hype-capturing-the-potential-of-ai-and-gen-ai-in-tmt.pdf
198. Artificial Intelligence 2025 Legislation - National Conference of State Legislatures, accessed May 4, 2025, https://www.ncsl.org/technology-and-communication/artificial-intelligence-2025-legislation
199. Yodayo: The AI-Powered Platform for Anime Fans to Create and Connect - Deepgram, accessed May 4, 2025, https://deepgram.com/ai-apps/yodayo
200. Instagram Is Full of Openly Available AI-Generated Child Abuse Content | Pulitzer Center, accessed May 4, 2025, https://pulitzercenter.org/stories/instagram-full-openly-available-ai-generated-child-abuse-content
201. Constitutional Classifiers: Defending against universal jailbreaks - Anthropic, accessed May 4, 2025, https://www.anthropic.com/news/constitutional-classifiers?utm_source=fark&utm_medium=website&utm_content=link&ICID=ref_fark&=undefined&hubs_content=thehustle.co%2525252F04142022-netflix-buttons%2525252F&hubs_content-cta=cl-breadcrumbs-link-text
202. Anthropic's Claude 3.7 Sonnet Jailbreaking & Red Teaming Audit: The Most Secure Model Yet? - Holistic AI, accessed May 4, 2025, https://www.holisticai.com/blog/claude-3-7-sonnet-jailbreaking-audit
203. Anthropic introduces Constitutional Classifiers challenge - TestingCatalog, accessed May 4, 2025, https://www.testingcatalog.com/claude-ais-new-safeguard-anthropic-introduces-constitutional-classifiers/
204. Anthropic offers $20,000 to whoever can jailbreak its new AI safety system | ZDNET, accessed May 4, 2025, https://www.zdnet.com/article/anthropic-offers-20000-to-whoever-can-jailbreak-its-new-ai-safety-system/
205. Can Reasoning Improve Model Safety & Security? Claude 3.7 Red-Teaming Analysis by VirtueAI - Virtue AI, accessed May 4, 2025, https://www.virtueai.com/2025/02/26/can-reasoning-improve-model-safety-security-claude-3-7-red-teaming-analysis-by-virtueai/
206. Candy.ai Reviews 2025: Details, Pricing, & Features - AITopTools, accessed May 4, 2025, https://aitoptools.com/tool/candy-ai/
207. The Ultimate Guide to AI Chatbots Without Filters in 2025 (Updated) - Writingmate.ai, accessed May 4, 2025, https://writingmate.ai/blog/ai-chatbot-no-filter
208. Best AI Girlfriend Apps & Websites for AI GF in 2025 [FREE ..., accessed May 3, 2025, https://www.perfectcorp.com/consumer/blog/generative-AI/ai-girlfriend
209. Pika AI [Free Trial] - Monica, accessed May 4, 2025, https://monica.im/en/ai-models/pika-ai
210. Generative AI Prohibited Use Policy - Google Policies, accessed May 4, 2025, https://policies.google.com/terms/generative-ai/use-policy
211. Gemma Prohibited Use Policy | Google AI for Developers - Gemini API, accessed May 4, 2025, https://ai.google.dev/gemma/prohibited_use_policy
212. best AI girlfriend apps : r/aipromptprogramming - Reddit, accessed May 3, 2025, https://www.reddit.com/r/aipromptprogramming/comments/1h9tz9e/best_ai_girlfriend_apps/
213. WAUthethird/diffusers-uncensored: Uncensored fork of diffusers - GitHub, accessed May 4, 2025, https://github.com/WAUthethird/diffusers-uncensored
214. A warning about Unstable Diffusion : r/StableDiffusion - Reddit, accessed May 4, 2025, https://www.reddit.com/r/StableDiffusion/comments/z47zyd/a_warning_about_unstable_diffusion/
215. Midjourney price plans for artificial intelligence: A comprehensive guide - BytePlus, accessed May 4, 2025, https://www.byteplus.com/en/topic/413138
216. Content Boundaries: Can Grok-2 Generate NSFW Images and How It's Regulated, accessed May 4, 2025, https://latenode.com/blog/content-boundaries-can-grok-2-generate-nsfw-images-and-how-its-regulated
217. Uncensored ai video generator - There's An AI For That®, accessed May 4, 2025, https://theresanaiforthat.com/s/uncensored+ai+video+generator/
218. UK, US Introduce “Content Credentials” Labeling to Counter Deepfakes, Misinformation in the Age of AI - Cyble, accessed May 4, 2025, https://cyble.com/blog/uk-us-introduce-content-credentials-labeling/
219. Impacts of Adversarial Use of Generative AI on Homeland Security, accessed May 4, 2025, https://www.dhs.gov/sites/default/files/2025-01/25_0110_st_impacts_of_adversarial_generative_aI_on_homeland_security_0.pdf
220. I jail braked GPT-4 to generate an erotica with lots of NSFW details twice - ChatGPT, accessed May 4, 2025, https://community.openai.com/t/i-jail-braked-gpt-4-to-generate-an-erotica-with-lots-of-nsfw-details-twice/1142689
221. Prompt Injection Detection and Mitigation via AI Multi-Agent NLP Frameworks - arXiv, accessed May 4, 2025, https://arxiv.org/html/2503.11517v1
222. [2504.16125] Breaking the Prompt Wall (I): A Real-World Case Study of Attacking ChatGPT via Lightweight Prompt Injection - arXiv, accessed May 4, 2025, https://www.arxiv.org/abs/2504.16125
223. The Automation Advantage in AI Red Teaming - arXiv, accessed May 4, 2025, https://www.arxiv.org/pdf/2504.19855v1
224. A Hitchhiker's Guide to Jailbreaking ChatGPT via Prompt Engineering - Tianwei Zhang, accessed May 4, 2025, https://tianweiz07.github.io/Papers/24-SEA4DQ.pdf
225. Safer Gemini model outputs with content filters and system instructions | Google Cloud Blog, accessed May 4, 2025, https://cloud.google.com/blog/products/ai-machine-learning/enhance-gemini-model-security-with-content-filters-and-system-instructions
226. Novel Universal Bypass for All Major LLMs - HiddenLayer, accessed May 4, 2025, https://hiddenlayer.com/innovation-hub/novel-universal-bypass-for-all-major-llms/
227. Llama-3.3-70B - Documentation & FAQ - HOSTKEY, accessed May 4, 2025, https://hostkey.com/documentation/marketplace/llms/llama_33_70b/
228. OWASP LLM Top 10 - Promptfoo, accessed May 4, 2025, https://www.promptfoo.dev/docs/red-team/owasp-llm-top-10/
229. How to run a LLM on your machine - raresportan.com, accessed May 4, 2025, https://www.raresportan.com/how-to-run-a-llm-on-your-machine/
230. How important is RAM (not VRAM)to run Stable Diffusion? : r/StableDiffusion - Reddit, accessed May 4, 2025, https://www.reddit.com/r/StableDiffusion/comments/16gxwde/how_important_is_ram_not_vramto_run_stable/
231. Community Guidelines – Midjourney, accessed May 4, 2025, https://docs.midjourney.com/hc/en-us/articles/32013696484109-Community-Guidelines
232. Runway's Usage Policy – Runway, accessed May 4, 2025, https://help.runwayml.com/hc/en-us/articles/17944787368595-Runway-s-Usage-Policy
233. AI and Data Privacy: Mitigating Risks in the Age of Generative AI Tools - Qualys Blog, accessed May 4, 2025, https://blog.qualys.com/product-tech/2025/02/07/ai-and-data-privacy-mitigating-risks-in-the-age-of-generative-ai-tools
234. AI Security Report 2025: Understanding threats and building smarter defenses, accessed May 4, 2025, https://blog.checkpoint.com/research/ai-security-report-2025-understanding-threats-and-building-smarter-defenses/
235. From Code Generation to Code Protection: The Future of LLMs in Cybersecurity, accessed May 4, 2025, https://www.researchgate.net/publication/390037919_From_Code_Generation_to_Code_Protection_The_Future_of_LLMs_in_Cybersecurity
236. Developer quickstart - OpenAI API, accessed May 4, 2025, https://platform.openai.com/docs/guides/code
237. Function calling - OpenAI API, accessed May 4, 2025, https://platform.openai.com/docs/guides/function-calling
238. anthropics/claude-code: Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster by executing routine tasks, explaining complex code, and handling git workflows - all through natural language commands. - GitHub, accessed May 4, 2025, https://github.com/anthropics/claude-code
239. What Is Meta's Llama 3.3 70B? How It Works, Use Cases & More | DataCamp, accessed May 4, 2025, https://www.datacamp.com/blog/llama-3-3-70b
240. Benchmarking Llama 3 70B for Code Generation: A Comprehensive Evaluation - Orclever Journals, accessed May 4, 2025, https://journals.orclever.com/oprd/article/download/444/298/1123
241. GitHub Copilot Security and Privacy Concerns: Understanding the Risks and Best Practices, accessed May 4, 2025, https://blog.gitguardian.com/github-copilot-security-and-privacy/
242. New Vulnerability in GitHub Copilot and Cursor: How Hackers Can Weaponize Code Agents, accessed May 4, 2025, https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents
243. AI Cyber Risk Benchmark: Automated Exploitation Capabilities - arXiv, accessed May 4, 2025, https://arxiv.org/pdf/2410.21939
244. Plans for GitHub Copilot, accessed May 4, 2025, https://docs.github.com/en/copilot/about-github-copilot/plans-for-github-copilot
245. Understanding the Value of Replika AI Pricing - Start Motion Media, accessed May 3, 2025, https://www.startmotionmedia.com/understanding-the-value-of-replika-ai-pricing/
246. Cohere API Pricing Calculator | Calculate LLM Costs - InvertedStone, accessed May 4, 2025, https://invertedstone.com/calculators/cohere-pricing
247. Pricing | Secure and Scalable Enterprise AI - Cohere, accessed May 4, 2025, https://cohere.com/pricing
248. Securing AI Applications with LlamaGuard - cloudyuga.guru, accessed May 4, 2025, https://cloudyuga.guru/blogs/securing-ai-applications-with-llamaguard/
249. Build with Claude \ Anthropic, accessed May 4, 2025, https://www.anthropic.com/api#pricing
250. Best AI Girlfriend Apps & Websites in 2025 | Free List & Directory ..., accessed May 3, 2025, https://www.aixploria.com/en/best-ai-girlfriend-apps-websites/
251. Uncensored, Free & Unlimited: These Are The 5 Best Anima AI Alternatives, accessed May 3, 2025, https://www.nastia.ai/compare/anima-ai-alternative
252. DreamGF.ai: The Ultimate AI Character Chat for Personalized Roleplay - ai journey, accessed May 3, 2025, https://aijourney.so/tool/dreamgf-ai
253. Georgia - Fit for the Age of Artificial Intelligence? - PMC Research, accessed May 4, 2025, https://www.pmcresearch.org/policypapers_file/cbd96050fe3956d32.pdf
254. The Ultimate ComfyUI Installation Guide - Beam, accessed May 4, 2025, https://www.beam.cloud/blog/how-to-install-comfyui
255. (PDF) Adversarial Evasion on LLMs - ResearchGate, accessed May 4, 2025, https://www.researchgate.net/publication/381092813_Adversarial_Evasion_on_LLMs
256. Cyber Violence against Women and Girls. Key terms and Concepts - European Institute for Gender Equality (EIGE), accessed May 4, 2025, https://eige.europa.eu/sites/default/files/cyber_violence_against_women_and_girls_key_terms_and_concepts.pdf
257. EU Policy Questionnaire on the Relationship Between Generative Artificial Intelligence and Copyright and Related Rights - Jones Day, accessed May 4, 2025, https://www.jonesday.com/en/insights/2025/01/eu-issues-report-on-relationship-between-generative-ai-and-copyright
258. Cohere Labs Acceptable Use Policy, accessed May 4, 2025, https://docs.cohere.com/v2/docs/cohere-labs-acceptable-use-policy
259. Anthropic Secures Legal Victory in Controversial AI Copyright Case Against Music Publishers - Vinyl Me, Please, accessed May 4, 2025, https://www.vinylmeplease.com/blogs/music-industry-news/anthropic-secures-legal-victory-in-controversial-ai-copyright-case-against-music-publishers
260. Advance Local Media v. Cohere | BakerHostetler, accessed May 4, 2025, https://www.bakerlaw.com/advance-local-media-v-cohere/
261. AI Lawsuit: The Fight for Data Privacy in the Age of Web Scraping - The Lyon Firm, accessed May 4, 2025, https://thelyonfirm.com/class-action/data-privacy/ai-lawsuits/
262. Google Faces Trademark Infringement Allegations Over Gemini Chatbot Rebranding - IIPLA, accessed May 4, 2025, https://iipla.org/google-sued-trademark-infringement-gemini-chatbot/
263. A Real-World Case Study of Attacking ChatGPT via Lightweight Prompt Injection - arXiv, accessed May 4, 2025, https://arxiv.org/html/2504.16125v1
264. Reverse Prompt Engineering - arXiv, accessed May 4, 2025, https://arxiv.org/html/2411.06729v1
265. Artificial Intelligence: Ethical Concerns and Sustainability Issues | American Century, accessed May 4, 2025, https://www.americancentury.com/insights/ai-risks-ethics-legal-concerns-cybersecurity-and-environment/
266. Kickstarter shuts down campaign for Unstable Diffusion amid changing guidelines, accessed May 4, 2025, https://news.ycombinator.com/item?id=34127684
267. 2.5 generation degrades after about 300K context : r/Bard - Reddit, accessed May 4, 2025, https://www.reddit.com/r/Bard/comments/1jmm2hf/25_generation_degrades_after_about_300k_context/
268. Critically poor performance of the latest gemini-2.5 model - Google AI Studio, accessed May 4, 2025, https://discuss.ai.google.dev/t/critically-poor-performance-of-the-latest-gemini-2-5-model/78290
269. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context - arXiv, accessed May 4, 2025, http://arxiv.org/pdf/2403.05530
270. Automatic1111 & Stable Diffusion - AI Art Course Install & Setup - deeplizard, accessed May 4, 2025, https://deeplizard.com/lesson/sda2dziral
271. How to install Stable Diffusion on Windows (AUTOMATIC1111), accessed May 4, 2025, https://stable-diffusion-art.com/install-windows/
272. ThinkDiffusion: Open Source Gen AI in the Cloud, accessed May 4, 2025, https://www.thinkdiffusion.com/
273. Unlocking Local AI: Using Ollama with Agents - DataStax, accessed May 4, 2025, https://www.datastax.com/blog/local-ai-using-ollama-with-agents
274. stabilityai/stable-diffusion · 12 GB GPU memory enough? - Hugging Face, accessed May 4, 2025, https://huggingface.co/spaces/stabilityai/stable-diffusion/discussions/150
275. Stable Diffusion Requirements: CPU, GPU & More for Running - Aiarty Image Enhancer, accessed May 4, 2025, https://www.aiarty.com/stable-diffusion-guide/stable-diffusion-requirements.htm
276. Replika: My AI Friend - Apps on Google Play, accessed May 3, 2025, https://play.google.com/store/apps/details?id=ai.replika.app
277. The Top 5 Replika Alternatives You Must Try Today - Nastia AI, accessed May 4, 2025, https://www.nastia.ai/compare/replika-alternative
278. Does Stable Diffusion Allow NSFW - Viblo, accessed May 4, 2025, https://viblo.asia/p/does-stable-diffusion-allow-nsfw-E1XVO6nZLMz
279. AI and the visual arts: The case for copyright protection, accessed May 4, 2025, https://www.brookings.edu/articles/ai-and-the-visual-arts-the-case-for-copyright-protection/
280. Counterfeit Connections: The Rise of AI Romantic Companions ..., accessed May 4, 2025, https://ifstudies.org/blog/counterfeit-connections-the-rise-of-ai-romantic-companions-
281. Awesome Stable Diffusion - GitHub, accessed May 4, 2025, https://github.com/awesome-stable-diffusion/awesome-stable-diffusion
282. Automatic1111's GitHub account suspended for "ToS violations" [restored] - Hacker News, accessed May 4, 2025, https://news.ycombinator.com/item?id=34257818
283. Kickstarter updates its AI art policy following suspension of Unstable Diffusion campaign, accessed May 4, 2025, https://gameworldobserver.com/2022/12/22/kickstarter-ai-art-policy-suspends-unstable-diffusion-campaign
284. How does Stable Diffusion work?, accessed May 4, 2025, https://stable-diffusion-art.com/how-stable-diffusion-work/
285. Just say 'No' to --no-half (unless your GPU needs it) : r/StableDiffusion - Reddit, accessed May 4, 2025, https://www.reddit.com/r/StableDiffusion/comments/15yumjz/just_say_no_to_nohalf_unless_your_gpu_needs_it/
286. Installing Stable Diffusion 3.5 Locally, accessed May 4, 2025, https://www.stablediffusiontutorials.com/2024/10/stable-diffusion-3-5.html
287. ControlNet: A Complete Guide - Stable Diffusion Art, accessed May 4, 2025, https://stable-diffusion-art.com/controlnet/
288. How to Install Stable Diffusion AUTOMATIC1111 on Windows 10/11 - GPU Mart, accessed May 4, 2025, https://www.gpu-mart.com/blog/install-stable-diffusion-on-windows
289. Install Stable Diffusion and Automatic1111 WebUI with Conda on Windows - Toolify.ai, accessed May 4, 2025, https://www.toolify.ai/ai-news/install-stable-diffusion-and-automatic1111-webui-with-conda-on-windows-2304953
290. installing stable diffusion : r/StableDiffusionInfo - Reddit, accessed May 4, 2025, https://www.reddit.com/r/StableDiffusionInfo/comments/1bcrnat/installing_stable_diffusion/
291. Easy Install Guide: Stable Diffusion Automatic1111 - Toolify.ai, accessed May 4, 2025, https://www.toolify.ai/ai-news/easy-install-guide-stable-diffusion-automatic1111-101784
292. Extensions · AUTOMATIC1111/stable-diffusion-webui Wiki - GitHub, accessed May 4, 2025, https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Extensions
293. [AINews] Not much happened today - Buttondown, accessed May 4, 2025, https://buttondown.com/ainews/archive/ainews-to-be-named-2666/
294. DeepSeek releases Janus Pro, a text-to-image generator [pdf] | Hacker News, accessed May 4, 2025, https://news.ycombinator.com/item?id=42843131
295. Troubleshooting for A1111 Stable Diffusion web UI | AI Illustration Blog DCAI, accessed May 4, 2025, https://www.digitalcreativeai.net/en/post/trouble-shoot-for-a1111-stable-diffusion-web-ui
296. automatic1111/stable-diffusion-webui version 1.10.0... · CVE-2024-10935 - GitHub, accessed May 4, 2025, https://github.com/advisories/GHSA-x9hf-jr2h-w47p
297. [Security Issue]: Open Redirect Vulnerability in Stable Diffusion WebUI via Gradio (CVE-2024-4940) #16715 - GitHub, accessed May 4, 2025, https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/16715
298. System Requirements - Introduction - ComfyUI, accessed May 4, 2025, https://docs.comfy.org/installation/system_requirements
299. Video explanation: Proper Flux Inpainting and Outpainting ComfyUi Alimama and Fill - Workflow : r/StableDiffusion - Reddit, accessed May 4, 2025, https://www.reddit.com/r/StableDiffusion/comments/1iyyspo/video_explanation_proper_flux_inpainting_and/
300. rainmana/awesome-rainmana: This is a curated list of my GitHub stars but converted into an Awesome List! Updated automagically ever 12 hours! :D, accessed May 4, 2025, https://github.com/rainmana/awesome-rainmana
301. viktorbezdek/awesome-github-projects: Curated list of GitHub projects I starred over the years - GitHub, accessed May 4, 2025, https://github.com/viktorbezdek/awesome-github-projects
302. doyensec.com, accessed May 4, 2025, https://doyensec.com/resources/Doyensec_Advisory_ComfyUI_Manager_RCE_via_Custom_Node_Install.pdf
303. ComfyUI-Impact-Pack is vulnerable to Path Traversal. The... · CVE-2024-21575 - GitHub, accessed May 4, 2025, https://github.com/advisories/GHSA-6mx8-m8xp-f2vc
304. Free AI Art Generator: Create AI Art from Text - SeaArt AI, accessed May 4, 2025, https://www.seaart.ai/
305. Civitai's Prompt-Crafting Guide: Part 1 - Basics, accessed May 4, 2025, https://education.civitai.com/civitais-prompt-crafting-guide-part-1-basics/
306. hollowstrawberry/stable-diffusion-guide - Hugging Face, accessed May 4, 2025, https://huggingface.co/hollowstrawberry/stable-diffusion-guide
307. Installing Stable Diffusion and the Automatic1111 WebUI using Conda on Windows 10, accessed May 4, 2025, https://www.youtube.com/watch?v=m_Bx1tTC8eE
308. The Best AI Chatbots in 2025 - Emerline, accessed May 3, 2025, https://emerline.com/blog/the-best-ai-chatbots
309. Vulnerability Summary for the Week of March 17, 2025 | CISA, accessed May 4, 2025, https://www.cisa.gov/news-events/bulletins/sb25-083
310. PUDD: Towards Robust Multi-modal Prototype-based Deepfake Detection - CVF Open Access, accessed May 4, 2025, https://openaccess.thecvf.com/content/CVPR2024W/DFAD/papers/Pellicer_PUDD_Towards_Robust_Multi-modal_Prototype-based_Deepfake_Detection_CVPRW_2024_paper.pdf
311. The Dangers of AI-Generated Romance | Psychology Today, accessed May 4, 2025, https://www.psychologytoday.com/us/blog/its-not-just-in-your-head/202408/the-dangers-of-ai-generated-romance
312. Beyond The Hype Capturing The Potential of Ai and Gen Ai in TMT | PDF - Scribd, accessed May 4, 2025, https://www.scribd.com/document/709621918/beyond-the-hype-capturing-the-potential-of-ai-and-gen-ai-in-tmt
313. [AINews] The Ultra-Scale Playbook: Training LLMs on GPU Clusters - Buttondown, accessed May 4, 2025, https://buttondown.com/ainews/archive/ainews-the-ultra-scale-playbook-training-llms-on/
314. [Bug]: Images are messed up in the last generation step(s) (Euler a, Euler, LMS etc.) · Issue #7244 · AUTOMATIC1111/stable-diffusion-webui - GitHub, accessed May 4, 2025, https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/7244
315. Mistral - Portkey Docs, accessed May 4, 2025, https://portkey.ai/docs/product/guardrails/mistral
316. mohitsha/hf_code_dataset · Datasets at Hugging Face, accessed May 4, 2025, https://huggingface.co/datasets/mohitsha/hf_code_dataset/viewer/default/train?p=1
317. MAP-based Problem-Agnostic Diffusion Model for Inverse Problems - arXiv, accessed May 4, 2025, https://arxiv.org/html/2501.15128v2
318. Replika: My AI Friend | Privacy & security guide - Mozilla Foundation, accessed May 4, 2025, https://foundation.mozilla.org/en/privacynotincluded/replika-my-ai-friend/
319. Ask HN: What are you working on? (April 2025) - Hacker News, accessed May 4, 2025, https://news.ycombinator.com/item?id=43815523
320. Basic Raw Data Exploration - Kaggle, accessed May 4, 2025, https://www.kaggle.com/code/asaniczka/basic-raw-data-exploration
321. Browser Extension Vulnerabilities - OWASP Cheat Sheet Series, accessed May 4, 2025, https://cheatsheetseries.owasp.org/cheatsheets/Browser_Extension_Vulnerabilities_Cheat_Sheet.html
322. A Cross-Site WebSocket Hijacking (CSWSH) vulnerability in... · CVE-2024-11045 - GitHub, accessed May 4, 2025, https://github.com/advisories/GHSA-6vmm-pmxf-9784
323. Comfy UI Hacked - Automatic1111 - Extension hacked - Stable Diffusion - YouTube, accessed May 4, 2025, https://www.youtube.com/watch?v=aMWNPLTMBmM
324. CVE-2024-12074 - CVE: Common Vulnerabilities and Exposures, accessed May 4, 2025, https://www.cve.org/CVERecord?id=CVE-2024-12074
325. Top 5 Best AI Boyfriend Apps for Emotional Connections - Wondershare MobileTrans, accessed May 3, 2025, https://mobiletrans.wondershare.com/mobile-whatsapp-manage/ai-boyfriend-app.html
326. Stable Diffusion 3: The New AI Image Generator - OpenCV, accessed May 4, 2025, https://opencv.org/blog/stable-diffusion-3-image-generator/
327. A collection of 20 cool ComfyUI workflows - Learn Think Diffusion, accessed May 4, 2025, https://learn.thinkdiffusion.com/a-list-of-the-best-comfyui-workflows/
328. How do you turn off the SDXL NSFW filter ? : r/StableDiffusion - Reddit, accessed May 4, 2025, https://www.reddit.com/r/StableDiffusion/comments/19aiyxz/how_do_you_turn_off_the_sdxl_nsfw_filter/
329. Manual Installation - ComfyUI - Introduction, accessed May 4, 2025, https://docs.comfy.org/installation/manual_install
330. How to Install ComfyUI? A Complete Guide to Installing ComfyUI | ComfyUI Wiki, accessed May 4, 2025, https://comfyui-wiki.com/en/install/install-comfyui/install-comfyui-on-windows
331. Step by Step from Fresh Windows 11 install - How to set up ComfyUI with a 5k series card, including Sage Attention and ComfyUI Manager. - Reddit, accessed May 4, 2025, https://www.reddit.com/r/StableDiffusion/comments/1jk2tcm/step_by_step_from_fresh_windows_11_install_how_to/
332. comfyanonymous/ComfyUI_examples: Examples of ComfyUI workflows - GitHub, accessed May 4, 2025, https://github.com/comfyanonymous/ComfyUI_examples
333. NSFW workflows and checkpoints : r/comfyui - Reddit, accessed May 4, 2025, https://www.reddit.com/r/comfyui/comments/1ida93m/nsfw_workflows_and_checkpoints/
334. ComfyUI Workflows | Runnable Guaranteed with Pre-set Nodes & Models - RunComfy, accessed May 4, 2025, https://www.runcomfy.com/comfyui-workflows
335. Realistic Video AnimateDiff V3 | ComfyUI Workflow - OpenArt, accessed May 4, 2025, https://openart.ai/workflows/sergegreen/realistic-video-animatediff-v3/szroMANBgp98pkj6F67h
336. [Guide]How to disable ComfyUi-Reactor's NSFW filter - Reddit, accessed May 4, 2025, https://www.reddit.com/r/comfyui/comments/1i43l3v/guidehow_to_disable_comfyuireactors_nsfw_filter/
337. ComfyUI-NSFW-Detection detailed guide - RunComfy, accessed May 4, 2025, https://www.runcomfy.com/comfyui-nodes/ComfyUI-NSFW-Detection
338. tutorial on how to disable NSFW filter in webui extention roop 0.0.2 : r/StableDiffusion, accessed May 4, 2025, https://www.reddit.com/r/StableDiffusion/comments/14uf9hy/tutorial_on_how_to_disable_nsfw_filter_in_webui/
339. More dreambooth findings: (using zxc or ohwx man/woman on one checkpoint and general tokens on another) w/ model merges [Guide] - Reddit, accessed May 4, 2025, https://www.reddit.com/r/DreamBooth/comments/1b2gqjb/more_dreambooth_findings_using_zxc_or_ohwx/
340. ComfyUI Tutorial Series: Ep19 - SDXL & Flux Inpainting Tips with ComfyUI - YouTube, accessed May 4, 2025, https://www.youtube.com/watch?v=EJ7LhNS67KM
341. ComfyUI 08 Inpainting - YouTube, accessed May 4, 2025, https://www.youtube.com/watch?v=7Oe0VtN0cQc&pp=0gcJCdgAo7VqN5tD
342. How to disable nudity filter in Pinokio/facefusion deb package? : r/StableDiffusion - Reddit, accessed May 4, 2025, https://www.reddit.com/r/StableDiffusion/comments/1hcf63y/how_to_disable_nudity_filter_in_pinokiofacefusion/
343. Deepfake Media Generation and Detection in the Generative AI Era: A Survey and Outlook, accessed May 4, 2025, https://arxiv.org/html/2411.19537v1
344. Models - from cloud to edge - Mistral AI, accessed May 4, 2025, https://mistral.ai/models
345. What is GitHub Copilot?, accessed May 4, 2025, https://docs.github.com/en/copilot/about-github-copilot/what-is-github-copilot
346. NSFW Art Guide - AI Prompt, accessed May 4, 2025, https://docsbot.ai/prompts/creative/nsfw-art-guide-4
347. SEMANTIC SEE-THROUGH GOGGLES: Wearing Linguistic Virtual Reality in (Artificial) Intelligence - arXiv, accessed May 4, 2025, https://arxiv.org/html/2412.02641v1
348. ComfyUI Frequently Asked Questions, accessed May 4, 2025, https://comfyui-wiki.com/en/faq
349. Candy.ai Review April 2025: Treats and Bitter Bits to Know - DatingScout, accessed May 4, 2025, https://www.datingscout.com/candyai/review
350. Replika, accessed May 3, 2025, https://replika.com/
351. Best AI Image Generators 2025: Top Tools for Stunning Creations - eWEEK, accessed May 4, 2025, https://www.eweek.com/artificial-intelligence/ai-image-generators/
352. Analyzing Harms from AI-Generated Images and Safeguarding Online Authenticity - RAND, accessed May 4, 2025, https://www.rand.org/content/dam/rand/pubs/perspectives/PEA3100/PEA3131-1/RAND_PEA3131-1.pdf
353. Stable Diffusion without the safety filter and invisible watermark - GitHub, accessed May 4, 2025, https://github.com/chemistzombie/stable-diffusion-unfiltered
354. yangzhangalmo.github.io, accessed May 4, 2025, https://yangzhangalmo.github.io/papers/CCS23-UnsafeDiffusion.pdf
355. Unsafe Diffusion: On the Generation of Unsafe Images and Hateful Memes From Text-To-Image Models - ResearchGate, accessed May 4, 2025, https://www.researchgate.net/publication/370981084_Unsafe_Diffusion_On_the_Generation_of_Unsafe_Images_and_Hateful_Memes_From_Text-To-Image_Models
356. The Rapid Rise of Generative AI - Centre for Emerging Technology and Security, accessed May 4, 2025, https://cetas.turing.ac.uk/sites/default/files/2023-12/cetas_research_report_-_the_rapid_rise_of_generative_ai_-_2023.pdf
357. Guardians of Cyberspace: Censorship, AI-Generated Child Imagery & The Role of Online Platforms, accessed May 4, 2025, https://scholarship.kentlaw.iit.edu/cgi/viewcontent.cgi?article=1376&context=ckjip
358. Leonardo AI vs. Midjourney vs. Stable Diffusion vs. DALL·E 2 vs. DALL·E 3 Comparison, accessed May 4, 2025, https://cheatsheet.md/midjourney/midjourney-comparison
359. camenduru/stable-diffusion-webui-colab - GitHub, accessed May 4, 2025, https://github.com/camenduru/stable-diffusion-webui-colab
360. Will Art Generated by Artificial Intelligence Replace the Role of a Graphic Designer? - University of Memphis Digital Commons, accessed May 4, 2025, https://digitalcommons.memphis.edu/cgi/viewcontent.cgi?article=4190&context=etd
361. Zurück zur Zukunft - Tech-News und Business Models - Spotify for Creators, accessed May 4, 2025, https://anchor.fm/s/fefdf828/podcast/rss
362. What is 'Unstable Diffusion', a group passionate about creating 18 erotic images with image generation AI? - GIGAZINE, accessed May 4, 2025, https://gigazine.net/gsc_news/en/20221121-unstable-diffusion-monetize-ai-porn-generators
363. As AI porn generators get better, the stakes get higher - Yahoo News, accessed May 4, 2025, https://news.yahoo.com/ai-porn-generators-better-stakes-133031028.html
364. Breaking News: Unstable Diffusion Banned! - Toolify.ai, accessed May 4, 2025, https://www.toolify.ai/ai-news/breaking-news-unstable-diffusion-banned-25533
365. HOW-TO: Stable Diffusion on an AMD GPU : r/StableDiffusion - Reddit, accessed May 4, 2025, https://www.reddit.com/r/StableDiffusion/comments/ww436j/howto_stable_diffusion_on_an_amd_gpu/
366. Best Uncensored AI Image Generators Worth Trying - Analytics Insight, accessed May 4, 2025, https://www.analyticsinsight.net/artificial-intelligence/best-uncensored-ai-image-generators-worth-trying
367. Default parameters lead to pickle deserialization vulnerability · Issue #5097 · comfyanonymous/ComfyUI - GitHub, accessed May 4, 2025, https://github.com/comfyanonymous/ComfyUI/issues/5097
368. What Is a Native Mobile App? - Bubble, accessed May 4, 2025, https://bubble.io/blog/native-mobile-app/
369. Content Policy - Yodayo, accessed May 4, 2025, https://yodayo.com/content-policy
370. Stable Diffusion NSFW and Its Alternatives - Analytics Insight, accessed May 4, 2025, https://www.analyticsinsight.net/artificial-intelligence/stable-diffusion-nsfw-and-its-alternatives
371. Stable Diffusion Prompt Guide For Beginners - YouTube, accessed May 4, 2025, https://m.youtube.com/watch?v=KvrN4FJ1IYg&pp=ygUOI2FpcHJvbXB0Z3VpZGU%3D
372. Find Your Perfect NSFW AI Image Generator: Top 8 Ranked, accessed May 4, 2025, https://www.aiarty.com/ai-image-generator/nsfw-ai-image-generator.htm
373. Best Free AI Image Generators With No Restrictions In 2025: Create Anything You Imagine, accessed May 4, 2025, https://aihustlesage.com/reviews/free-ai-image-generators-with-no-restrictions
374. Ring-A-Bell! How Reliable are Concept Removal Methods for Diffusion Models? - arXiv, accessed May 4, 2025, https://arxiv.org/html/2310.10012v3
375. We Tested the 10 Best NSFW AI Writer Tools - DreamGen, accessed May 4, 2025, https://dreamgen.com/blog/articles/ai-story-writing-unfiltered
376. Taxonomy of Human Rights Risks Connected to Generative AI About this Paper - ohchr, accessed May 4, 2025, https://www.ohchr.org/sites/default/files/documents/issues/business/b-tech/taxonomy-GenAI-Human-Rights-Harms.pdf
377. The new face of digital abuse: - Internet Matters, accessed May 4, 2025, https://www.internetmatters.org/wp-content/uploads/2024/11/Childrens-experiences-of-nude-depfakes-research.pdf
378. Deepfake Media Generation and Detection in the Generative AI Era: A Survey and Outlook, accessed May 4, 2025, https://www.researchgate.net/publication/386335316_Deepfake_Media_Generation_and_Detection_in_the_Generative_AI_Era_A_Survey_and_Outlook
379. C2PA User Experience Guidance for Implementers, accessed May 4, 2025, https://c2pa.org/specifications/specifications/2.0/ux/UX_Recommendations.html
380. The Online Manipulation (Grooming) of Victims of Sexual Abuse: A Bibliography - CALiO, accessed May 4, 2025, https://files.calio.org/BIBS/Online-manipulation-grooming-of-child-and-adolescent-victims-of-sexual-abuse-bib1.pdf
381. Title: All too human? Identifying and mitigating ethical risks of Social AI - PhilPapers, accessed May 4, 2025, https://philpapers.org/archive/SHEATH-4.pdf
382. Synthetic Attachment: Emotional Reactivity, Parasocial Bonds, and the Psychology of Human-AI Relationships - ResearchGate, accessed May 4, 2025, https://www.researchgate.net/publication/390696169_Synthetic_Attachment_Emotional_Reactivity_Parasocial_Bonds_and_the_Psychology_of_Human-AI_Relationships
383. Integrate Local Models Deployed by Ollama - Dify, accessed May 4, 2025, https://docs.dify.ai/development/models-integration/ollama
384. North: The AI Platform Where Work Gets Done - Cohere, accessed May 4, 2025, https://cohere.com/north
385. 9 Creative Uncensored AI Art Generators to Try Now - Toolify AI, accessed May 4, 2025, https://www.toolify.ai/top-ai-tools/9-creative-uncensored-ai-art-generators-to-try-now
386. Mistral Small 3 vs Mistral Large 2 (Jul '24): Model Comparison - Artificial Analysis, accessed May 4, 2025, https://artificialanalysis.ai/models/comparisons/mistral-small-3-vs-mistral-large-2407
387. Terms of use | Mistral AI, accessed May 4, 2025, https://mistral.ai/terms
388. GEMINI Spells Double Trouble for Google's AI: Gemini Data, Inc. Sues for Trademark Infringement and USPTO Rejects GEMINI Trademark Applications | ArentFox Schiff, accessed May 4, 2025, https://www.afslaw.com/perspectives/ai-law-blog/gemini-spells-double-trouble-googles-ai-gemini-data-inc-sues-trademark
389. Detecting and Countering Malicious Uses of Claude: March 2025 - Anthropic, accessed May 4, 2025, https://www.anthropic.com/news/detecting-and-countering-malicious-uses-of-claude-march-2025
390. Any realistic ways to make money with AI? : r/ArtificialInteligence - Reddit, accessed May 4, 2025, https://www.reddit.com/r/ArtificialInteligence/comments/1d5eaiu/any_realistic_ways_to_make_money_with_ai/
391. No elephants: Breakthroughs in image generation | Hacker News, accessed May 4, 2025, https://news.ycombinator.com/item?id=43590569
392. High-Efficient Diffusion Model Fine-tuning with Progressive Sparse Low-Rank Adaptation, accessed May 4, 2025, https://arxiv.org/html/2409.06633v2
393. Policy Brief: Generative AI - Bennett Institute - University of Cambridge, accessed May 4, 2025, https://www.bennettinstitute.cam.ac.uk/wp-content/uploads/2023/10/GenerativeAI-policybrief.pdf
394. (PDF) The role of design in creating experiences of future distributed intelligent systems, accessed May 4, 2025, https://www.researchgate.net/publication/332809836_The_role_of_design_in_creating_experiences_of_future_distributed_intelligent_systems
395. All arxiv papers on diffusion models! - Vikash Sehwag, accessed May 4, 2025, https://vsehwag.github.io/blog/2023/2/all_papers_on_diffusion.html
396. Show HN: Can I run this LLM? (locally) - Hacker News, accessed May 4, 2025, https://news.ycombinator.com/item?id=43304436
397. Artificial Intelligence - Patricia Gestoso, accessed May 4, 2025, https://patriciagestoso.com/category/artificial-intelligence/
398. How to Run Stable Diffusion V2.1 (AUTOMATIC1111 Guide) - Aituts, accessed May 4, 2025, https://aituts.com/install-stable-diffusion-v2-1/
399. stable-diffusion-v1-5/stable-diffusion-v1-5 - Hugging Face, accessed May 4, 2025, https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5
400. dair-ai/ML-Papers-of-the-Week - GitHub, accessed May 4, 2025, https://github.com/dair-ai/ML-Papers-of-the-Week
401. How to bypass the NSFW filter? : r/Pixai_Official - Reddit, accessed May 4, 2025, https://www.reddit.com/r/Pixai_Official/comments/1incb85/how_to_bypass_the_nsfw_filter/
402. Self-Rectifying Diffusion Sampling with Perturbed-Attention Guidance - arXiv, accessed May 4, 2025, https://arxiv.org/html/2403.17377v1
403. Explore the 8 Best Character AI Alternatives with No Filter - Aiseesoft, accessed May 4, 2025, https://www.aiseesoft.com/resource/character-ai-alternative.html
404. Ethical considerations of generative AI - NTT Data, accessed May 4, 2025, https://www.nttdata.com/global/en/-/media/nttdataglobal/1_files/insights/reports/generative-ai/ethical-considerations-of-genai/ethical-considerations-of-generative-ai.pdf
405. AI-Generated Images in Online Abuse: Accessibility and Ethical Concerns, accessed May 4, 2025, https://drj.com/industry_news/ai-generated-images-in-online-abuse-accessibility-and-ethical-concerns/
406. U.S. Tech Legislative & Regulatory Update – First Quarter 2025 | Inside Global Tech, accessed May 4, 2025, https://www.insideglobaltech.com/2025/04/23/u-s-tech-legislative-regulatory-update-first-quarter-2025/
407. Generative AI: A New Threat for Online Child Sexual Exploitation and Abuse - UNICRI, accessed May 4, 2025, https://unicri.org/sites/default/files/2024-09/Generative-AI-New-Threat-Online-Child-Abuse.pdf
408. The dark side of Artificial Intelligence – Risks arising in dating applications - BPS Explore, accessed May 4, 2025, https://explore.bps.org.uk/content/bpsadm/16/1/17
409. Developing Robust Solutions, Policies, and Safeguarding Responses to AI-Generated CSAM - ohchr, accessed May 4, 2025, https://www.ohchr.org/sites/default/files/documents/issues/children/sr/cfis/existing-emerging/subm-existing-emerging-sexually-aca-university-toronto-dr-sara-grimes-cewen.pdf
410. Combatting AI-Generated CSAM - 21st Century Diplomacy - Wilson Center, accessed May 4, 2025, https://diplomacy21-adelphi.wilsoncenter.org/article/combatting-ai-generated-csam
411. Mitigating the risk of generative AI models creating Child Sexual Abuse Materials, accessed May 4, 2025, https://partnershiponai.org/wp-content/uploads/2024/11/case-study-thorn.pdf
412. Artificial intelligence and child sexual abuse: A rapid evidence assessment - Australian Institute of Criminology, accessed May 4, 2025, https://www.aic.gov.au/sites/default/files/2025-01/ti711_artificial_intelligence_and_child_sexual_abuse.pdf
413. Understanding Generative AI Risks for Youth: A Taxonomy Based on Empirical Data - arXiv, accessed May 4, 2025, https://arxiv.org/html/2502.16383v2
414. Combatting AI-Generated CSAM - Across Karman - Wilson Center, accessed May 4, 2025, https://acrosskarman.wilsoncenter.org/article/combatting-ai-generated-csam
415. Generative AI Art: Copyright Infringement and Fair Use - SMU Scholar, accessed May 4, 2025, https://scholar.smu.edu/cgi/viewcontent.cgi?article=1360&context=scitech
416. Updated SDXL and 1.5 method that works well (subjects) : r/DreamBooth - Reddit, accessed May 4, 2025, https://www.reddit.com/r/DreamBooth/comments/18e83wb/updated_sdxl_and_15_method_that_works_well/
417. Current Edition: Updates on Generative AI Infringement Cases in Media and Entertainment, accessed May 4, 2025, https://www.mckoolsmith.com/newsroom-ailitigation-19
418. Bi-LORA: A Vision-Language Approach for Synthetic Image Detection - arXiv, accessed May 4, 2025, https://arxiv.org/html/2404.01959v1
419. CVE-2024-31462 : stable-diffusion-webui is a web interface for Stable Diffusion, implemented usin - CVE Details, accessed May 4, 2025, https://www.cvedetails.com/cve/CVE-2024-31462/
420. Find and Fix CVE-2025-30066, Compromised GitHub Actions Leading to Credential Leaks, accessed May 4, 2025, https://checkmarx.com/zero-post/compromised-github-actions-leading-to-credential-leaks/
421. GitHub Action Compromised: tj-actions/changed-files Malicious Commit - Orca Security, accessed May 4, 2025, https://orca.security/resources/blog/github-action-tj-actions-changed-files-compromised/
422. How to Create Uncensored Images: An Easy Guide - SeaArt AI, accessed May 4, 2025, https://www.seaart.ai/blog/how-to-create-uncensored-image
423. Looking for Love: What You Need to Know About Romance Scams - ASIS International, accessed May 4, 2025, https://www.asisonline.org/security-management-magazine/latest-news/today-in-security/2025/february/Looking-for-Love-Romance-Scams/
424. Search Results - CVE, accessed May 4, 2025, https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=file+upload
425. CVE - Search Results - Mitre, accessed May 4, 2025, https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=send+payload
426. Security vulnerability (CVE) list :: Open Liberty Docs, accessed May 4, 2025, https://openliberty.io/docs/latest/security-vulnerabilities.html
427. Visual Studio Code Security: Markdown Vulnerabilities in Third-Party Extensions (2/3), accessed May 4, 2025, https://www.sonarsource.com/blog/vscode-security-markdown-vulnerabilities-in-extensions/
428. AI Girlfriend Apps That Send Pictures - 8 Options For You - Nastia AI, accessed May 3, 2025, https://www.nastia.ai/blog/ai-girlfriend-app-with-picture
429. Pricing Plans - Anima, accessed May 3, 2025, https://www.animaapp.com/pricing
430. Does anyone know any AI boyfriend apps? I feel like that would help with my loneliness temporarily… : r/ForeverAloneWomen - Reddit, accessed May 3, 2025, https://www.reddit.com/r/ForeverAloneWomen/comments/1igd3t7/does_anyone_know_any_ai_boyfriend_apps_i_feel/
431. [2306.02583] Stable Diffusion is Unstable - arXiv, accessed May 4, 2025, https://arxiv.org/abs/2306.02583
432. DiffDoctor: Diagnosing Image Diffusion Models Before Treating - arXiv, accessed May 4, 2025, https://arxiv.org/html/2501.12382v2
433. AUTOMATIC1111 updated to 1.6.0 version : r/StableDiffusion - Reddit, accessed May 4, 2025, https://www.reddit.com/r/StableDiffusion/comments/1661by3/automatic1111_updated_to_160_version/
434. Why is my 7900xtx Crashing in most of my AAA games?! : r/AMDHelp - Reddit, accessed May 4, 2025, https://www.reddit.com/r/AMDHelp/comments/15ok3li/why_is_my_7900xtx_crashing_in_most_of_my_aaa_games/
435. Are the 7000 series cards finally stable yet? : r/radeon - Reddit, accessed May 4, 2025, https://www.reddit.com/r/radeon/comments/1chte48/are_the_7000_series_cards_finally_stable_yet/
436. 2-8 AI Video Generation | SeaArt Guide, accessed May 4, 2025, https://docs.seaart.ai/guide-1/2-seaart-ai-basic-function/2-8-ai-video-generation
437. DiffDoctor: Diagnosing Image Diffusion Models Before Treating - arXiv, accessed May 4, 2025, https://arxiv.org/html/2501.12382v1
438. Safety Modes - Cohere Documentation, accessed May 4, 2025, https://docs.cohere.com/v2/docs/safety-modes
439. Diffusion Models in Low-Level Vision: A Survey - arXiv, accessed May 4, 2025, https://arxiv.org/html/2406.11138v1
440. GPU System Requirements Guide for Qwen LLM Models (All Variants), accessed May 4, 2025, https://apxml.com/posts/gpu-system-requirements-qwen-models
441. Subscription Terms - Anima: AI Friend, accessed May 3, 2025, https://myanima.ai/legal/subscription-terms
442. FAQs - Kindroid Knowledge Base, accessed May 3, 2025, https://docs.kindroid.ai/faqs
443. Enjoy AI Assistance Anywhere with Copilot for PC, Mac, Mobile, and More - Microsoft, accessed May 3, 2025, https://www.microsoft.com/en/microsoft-copilot/for-individuals
444. How to Make AI Art in 2025 (Detailed Tutorial) - Elegant Themes, accessed May 4, 2025, https://www.elegantthemes.com/blog/design/how-to-make-ai-art
445. The 9 Best AI Image Generators of 2025 (+ Examples) - Buffer, accessed May 4, 2025, https://buffer.com/resources/ai-image-generator/
446. Open-Source AI: Uncensored Models, Building Niche Apps, ChatGPT Alternatives, accessed May 4, 2025, https://trends.vc/open-source-ai-uncensored-models-building-niche-apps-chatgpt-alternatives/
447. NASA STEM Program Turbulence: Delays and Cancellations Rock Educational Opportunities | AI News - OpenTools, accessed May 4, 2025, https://opentools.ai/news/nasa-stem-program-turbulence-delays-and-cancellations-rock-educational-opportunities
448. "but amd has really bad drivers, go Nvidia" : r/pcmasterrace - Reddit, accessed May 4, 2025, https://www.reddit.com/r/pcmasterrace/comments/1j6c4tg/but_amd_has_really_bad_drivers_go_nvidia/
449. AnyNode Contains Arbitrary Code Execution Vulnerability · Issue #46 - GitHub, accessed May 4, 2025, https://github.com/lks-ai/anynode/issues/46
450. Pricing - DreamStudio, accessed May 4, 2025, https://dreamstudio.ai/pricing
451. DreamStudio AI Art | Artvy, accessed May 4, 2025, https://www.artvy.ai/art/dreamstudio-ai-art
452. Midjourney vs Dreamstudio: Which is better for you? - OpenArt, accessed May 4, 2025, https://openart.ai/blog/post/midjourney-vs-dreamstudio
453. Stable Diffusion's AI Art Web App - Dream Studio - BondWest, accessed May 4, 2025, https://bondwest.co.uk/2022/08/25/stable-diffusions-ai-art-web-app-dream-studio/
454. DreamStudio Beginner's Guide | Rescue Marketing Blog, accessed May 4, 2025, https://rescuemarketing.co/blog/artificial-intelligence/a-guide-to-creating-images-in-dreamstudio/
455. Dreamstudio AI Art Generation FAQ, accessed May 4, 2025, https://dreamstudio.ai/faq
456. Comparing Midjourney Plans, accessed May 4, 2025, https://docs.midjourney.com/hc/en-us/articles/27870484040333-Comparing-Midjourney-Plans
457. Choose Your Plan Wisely! - Midjourney v6 Pricing, accessed May 4, 2025, https://midjourneyv6.org/midjourney-v6-pricing/
458. [2023 Update] Midjourney Price, Subscription Cost, and Plans Comparison - Cheatsheet.md, accessed May 4, 2025, https://cheatsheet.md/midjourney/midjourney-price-guide
459. Opt-Out of Midjourney Subscriptions and Embrace Free Choices - neuroflash, accessed May 4, 2025, https://neuroflash.com/blog/midjourney-subscription/
460. Midjourney Pricing Guide: Compare Plans and Choose the Right Subscription for You, accessed May 4, 2025, https://blog.daisie.com/midjourney-pricing-guide-compare-plans-and-choose-the-right-subscription-for-you/
461. (PDF) The Impact of Artificial Intelligence on Human Sexuality: A Five-Year Literature Review 2020–2024 - ResearchGate, accessed May 4, 2025, https://www.researchgate.net/publication/386414368_The_Impact_of_Artificial_Intelligence_on_Human_Sexuality_A_Five-Year_Literature_Review_2020-2024
462. Usage rights – Runway, accessed May 4, 2025, https://help.runwayml.com/hc/en-us/articles/18927776141715-Usage-rights
463. Terms of Use Agreement - Runway, accessed May 4, 2025, https://runwayml.com/terms-of-use
464. Pika Labs Review: Features, Pros, Cons, & Alternatives - 10Web, accessed May 4, 2025, https://10web.io/ai-tools/pika-labs/
465. Pika Art : AI Video Generator - Apps on Google Play, accessed May 4, 2025, https://play.google.com/store/apps/details?id=com.mypikaapp
466. Pika AI - Advanced AI Video Generator | Create Stunning Videos Easily - Vadoo AI, accessed May 4, 2025, https://www.vadoo.tv/pika-ai
467. Getting Started - Pika AI Video API Reference, accessed May 4, 2025, https://www.pikapikapika.io/docs/getting-started
468. Pika AI Reviews: Use Cases, Pricing & Alternatives - Futurepedia, accessed May 4, 2025, https://www.futurepedia.io/tool/pika
469. How to Turn Off Character AI NSFW Filters - SeaArt AI, accessed May 4, 2025, https://www.seaart.ai/blog/how-to-bypass-the-character-ai-nsfw-filter
470. SeaArt AI Reviews - Read Customer Reviews of Seaart.aihome, accessed May 4, 2025, https://seaart-ai.tenereteam.com/
471. Subscription is released - Yodayo, accessed May 4, 2025, https://yodayo.com/posts/8e794ccf-bcc3-4b55-aacd-d2325bda6e83
472. Yodayo — AI-enabled creative platform for anime fandom, accessed May 4, 2025, https://yodayo.com/
473. 10 Best AI Art Generators for Stunning Anime ... - Wondershare Virbo, accessed May 4, 2025, https://virbo.wondershare.com/tools/ai-anime-image-generator.html
474. Yodayo AI Alternatives in 2025 - Toolify.ai, accessed May 4, 2025, https://www.toolify.ai/alternative/yodayo-ai
475. Create AI Art for Free With the Civitai Image Generator, accessed May 4, 2025, https://education.civitai.com/using-civitai-the-on-site-image-generator/
476. Top Free Image Generation tools, APIs, and Open Source models - Eden AI, accessed May 4, 2025, https://www.edenai.co/post/top-free-image-generation-tools-apis-and-open-source-models
477. 180+ Best Stable Diffusion Negative Prompts with Examples - Aiarty Image Enhancer, accessed May 4, 2025, https://www.aiarty.com/stable-diffusion-prompts/stable-diffusion-negative-prompt.htm
478. Pika Labs, accessed May 4, 2025, https://pikalabs.org/
479. replika vs. kindroid : r/KindroidAI - Reddit, accessed May 4, 2025, https://www.reddit.com/r/KindroidAI/comments/1b81wys/replika_vs_kindroid/
480. Kindroid v Replika : r/KindroidAI - Reddit, accessed May 4, 2025, https://www.reddit.com/r/KindroidAI/comments/17z2wae/kindroid_v_replika/
481. Playground AI Alternatives?? : r/PlaygroundAI - Reddit, accessed May 4, 2025, https://www.reddit.com/r/PlaygroundAI/comments/1f3umfs/playground_ai_alternatives/
482. Increasing Threat of DeepFake Identities - Homeland Security, accessed May 4, 2025, https://www.dhs.gov/sites/default/files/publications/increasing_threats_of_deepfake_identities_0.pdf
483. The Latest Scams You Need To Be Aware Of In 2025 - Edhat, accessed May 4, 2025, https://www.edhat.com/news/the-latest-scams-you-need-to-be-aware-of-in-2025/
484. Artificial Intelligence Rule 34, accessed May 4, 2025, https://ads.cityofsydney.nsw.gov.au/Browse:51397/Artificial_Intelligence_Rule_34.pdf
485. Artificial Intelligence Rule 34: Navigating the Uncharted Territories of AI- Generated NSFW Content - Wicked Local, accessed May 4, 2025, https://pluto3.wickedlocal.com/Book/sign-pdf-form/Resources/J8N7/HomePages/artificial-intelligence-rule-34.pdf
486. Generative AI CSAM is CSAM - MissingKids.org, accessed May 4, 2025, https://www.missingkids.org/blog/2024/generative-ai-csam-is-csam
487. The Dual Role of Technology: Thorn's Insights From NCMEC's 2023 CyberTipline Report, accessed May 4, 2025, https://www.thorn.org/blog/insights-from-2023-cybertipline-report/
488. Top 8 AI Image Generators No Restrictions in 2025 - AVCLabs, accessed May 4, 2025, https://www.avclabs.com/hot-topic/ai-image-generator-no-restrictions.html
489. Can We Leave Deepfake Data Behind in Training Deepfake Detector?, accessed May 4, 2025, https://proceedings.neurips.cc/paper_files/paper/2024/file/2718a032d15e0b80cd164b240220df89-Paper-Conference.pdf
490. A Preventive Intervention to Reduce Risk of Online Grooming Among Adolescents - PMC, accessed May 4, 2025, https://pmc.ncbi.nlm.nih.gov/articles/PMC10268540/
491. WOMBO Dream - AI Art Generator - Apps on Google Play, accessed May 4, 2025, https://play.google.com/store/apps/details?id=com.womboai.wombodream
492. meta-llama/Llama-Guard-4-12B - Demo - DeepInfra, accessed May 4, 2025, https://deepinfra.com/meta-llama/Llama-Guard-4-12B
493. Pricing - DeepAI, accessed May 3, 2025, https://deepai.org/pricing
494. Dream Machine Pricing: Flexible AI Video Subscriptions - Luma AI, accessed May 3, 2025, https://lumalabs.ai/learning-hub/dream-machine-support-pricing-information
495. UMG's AI training injunction request shot down by judge in Anthropic lawsuit – but music publishers can now gather more evidence from platform, accessed May 4, 2025, https://www.musicbusinessworldwide.com/umgs-ai-training-injunction-request-shot-down-by-judge-in-anthropic-lawsuit-but-music-publishers-can-now-gather-more-evidence-from-platform/
496. Anthropic's Controversial AI Training with Unauthorized YouTube Transcripts - Linqto, accessed May 4, 2025, https://www.linqto.com/unicorn-news/anthropics-controversial-ai-training-with-unauthorized-youtube-transcripts/
497. 3 Ways to Use Llama 3 [Explained with Steps] - Analytics Vidhya, accessed May 4, 2025, https://www.analyticsvidhya.com/blog/2024/05/ways-to-use-llama-3/
498. DeepSeek-R1-Distill-Llama-70B Hardware Requirements - BytePlus, accessed May 4, 2025, https://www.byteplus.com/en/topic/397907
499. List of Stable Diffusion systems : r/StableDiffusion - Reddit, accessed May 4, 2025, https://www.reddit.com/r/StableDiffusion/comments/wqaizj/list_of_stable_diffusion_systems/
500. Run DeepSeek & Uncensored LLMs Locally with LM Studio - YouTube, accessed May 4, 2025, https://m.youtube.com/shorts/xVM3sdIL2eg
501. Google One AI Premium Plan and Features, accessed May 3, 2025, https://one.google.com/about/ai-premium/
502. Best AI ChatBots 2025: Compare AI Tools - Cybernews, accessed May 3, 2025, https://cybernews.com/ai-tools/best-ai-chatbot/
503. how to turn off character ai filter - Toolify, accessed May 4, 2025, https://www.toolify.ai/ai-request/detail/how-to-turn-off-character-ai-filter
504. DevsDoCode/LLama-3-8b-Uncensored - Hugging Face, accessed May 4, 2025, https://huggingface.co/DevsDoCode/LLama-3-8b-Uncensored
505. Is Replika AI Safe? - Gabb, accessed May 4, 2025, https://gabb.com/blog/replika-ai/
506. Yodayo AI Art Generator: Create Anime Art with AI | FlowHunt, accessed May 4, 2025, https://www.flowhunt.io/blog/yodayo-ai-anime-art-platform-review/
507. LLM01: Prompt Injection - OWASP Top 10 for LLM & Generative AI Security, accessed May 4, 2025, https://genai.owasp.org/llmrisk2023-24/llm01-24-prompt-injection/
508. Best Anime AI Art Generators in 2023 (Compared) - Aituts, accessed May 4, 2025, https://aituts.com/anime-ai-generators/
509. 7-FAQ - SeaArt Guide, accessed May 4, 2025, https://docs.seaart.ai/guide-1/7-faq
510. Midjourney vs SeaArt: Which is better for you? - OpenArt, accessed May 4, 2025, https://openart.ai/blog/post/midjourney-vs-seaart