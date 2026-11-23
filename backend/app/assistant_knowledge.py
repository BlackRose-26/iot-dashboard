"""Reviewed public system context. No private configuration, credentials or live records."""
from typing import Literal

Knowledge = Literal['gameplay', 'registration', 'queue_flow', 'architecture', 'dashboard', 'privacy', 'offline', 'results', 'assistant', 'memory', 'training']
Social = Literal['greeting', 'thanks', 'identity', 'help', 'acknowledge', 'farewell', 'wellbeing']

# Curated context is code-reviewed, not an arbitrary filesystem/document retrieval tool.
KNOWLEDGE = {
    'training': ('Reviewed training examples',
        'After an eligible reply, open Dashboard Settings and choose Review last eligible answer. Inspect the sanitized input, correct the routing label and save it as pending. In Training examples, explicitly review and approve it before exporting the current approved JSONL dataset. Only approved vocabulary and typed routing context are included, never raw chat, player records or metric answers. Examples are private to your admin account and separate from conversation memory. When memory is enabled, current approved examples help interpret similar future questions. Exact matching corrections can route locally; related examples guide Ollama. Exporting prepares examples; it does not train, import or activate a new Ollama model.',
        'Pagkatapos ng eligible reply, buksan ang Dashboard Settings at piliin ang Review last eligible answer. Tingnan ang sanitized input, itama ang routing label at i-save bilang pending. Sa Training examples, i-review at i-approve ito bago i-export ang current approved JSONL dataset. Approved words at typed routing context lang ang kasama, hindi raw chat, player records o metric answers. Private ito sa admin account mo at hiwalay sa conversation memory. Kapag enabled ang memory, ginagamit ang current approved examples para mas maintindihan ang susunod na tanong. Paghahanda ng examples ang export; hindi pa nito tina-train o pinapalitan ang Ollama model.',
        'assistant-training.md'),
    'gameplay': ('How the game works',
        'Stack Moko Baby is an ESP32 LED-matrix stacker controlled by a physical button. Players line up moving LED rows to build a stack. The ESP32 owns game timing; the backend validates submitted placement evidence before accepting a score. Numeric game settings are still proposals until play-tested.',
        'Ang Stack Moko Baby ay ESP32 LED-matrix stacker na may physical button. Itinatapat ng player ang gumagalaw na LED rows para bumuo ng stack. ESP32 ang may hawak ng game timing; backend ang nagva-validate ng placement evidence bago tanggapin ang score. Proposed pa ang numeric settings hanggang ma-play-test.',
        'functional-specification.md'),
    'registration': ('Player entry and registration',
        'Players scan the operator’s event QR using the camera or an uploaded image, then register with a nickname and a required private student ID. They receive their own queue ticket. Players cannot access the admin dashboard.',
        'I-scan ng player ang event QR ng operator gamit ang camera o uploaded image, saka mag-register gamit ang nickname at required private student ID. Makukuha nila ang sarili nilang queue ticket. Hindi nila maa-access ang admin dashboard.',
        'player-flow-and-access.md'),
    'queue_flow': ('How the queue works',
        'Registration saves a queue place; it does not immediately start the game. An operator calls the next waiting player when admissions are open and the cabinet is ready. The device must accept its reservation command before the physical button can start that round. Uncertain device reservations are held for review; automatic safe release and physical firmware integration remain pending. I can explain the queue, but cannot call or skip a player for you.',
        'Nagbibigay ng puwesto sa pila ang registration; hindi nito agad sini-start ang laro. Operator ang tatawag sa susunod kapag open ang admissions at ready ang cabinet. Kailangang tanggapin ng device ang reservation command bago mag-start gamit ang physical button. Naka-hold for review ang uncertain reservations; pending pa ang safe release at physical firmware integration. Pwede kong ipaliwanag ang pila, pero hindi ako makakatawag o makaka-skip ng player.',
        'player-flow-and-access.md'),
    'architecture': ('System architecture',
        'The dashboard uses React with JavaScript and Vite. FastAPI/Python serves the backend, with XAMPP’s MariaDB database. Ollama runs locally for question interpretation. The ESP32 is the planned physical game controller; simulator observations do not prove that real hardware is connected.',
        'React JavaScript at Vite ang frontend; FastAPI/Python ang backend at MariaDB ng XAMPP ang database. Local Ollama ang tumutulong umintindi ng tanong. ESP32 ang planned physical game controller; hindi patunay ng real hardware connection ang simulator observations.',
        'tech-stack.md'),
    'dashboard': ('Dashboard and roles',
        'The private admin dashboard covers the event overview, analytics, queue, sessions, cabinet observations and settings. Its font family is Open Sans Variable. Analytics can show completed rounds, win rate, scores, overlap accuracy, level failures and activity trends. Chat automatically checks all available result sources and the full event unless you ask for a narrower scope. Simulator and physical-device metrics stay separately labelled; match the answer scope when comparing charts. Absent telemetry stays unknown.',
        'Private sa admin ang dashboard para sa overview, analytics, pila, sessions, cabinet observations at settings. Open Sans Variable ang font family nito. Makikita sa analytics ang completed rounds, win rate, scores, overlap accuracy, level failures at activity trends. Automatic na sinusuri ng chat ang buong event at lahat ng available result sources maliban kung mas specific ang tanong. Hiwalay at labelled ang simulator at physical-device metrics; itugma ang answer scope sa charts. Unknown pa rin ang walang telemetry.',
        'dashboard-design.md'),
    'privacy': ('Privacy and access',
        'Student IDs are required to prevent duplicate event registration. They are private and encrypted at rest in the XAMPP MariaDB database. The assistant has no identity-decryption, credential or game-control tools. Players use their own registration and queue flow; administrator access requires sign-in. Keep identifiers and credentials out of chat.',
        'Required ang student IDs para maiwasan ang duplicate registration. Private at encrypted at rest ito sa XAMPP MariaDB database. Walang identity-decryption, credential o game-control tools ang assistant. Sariling registration at queue flow ang gamit ng players; kailangang mag-sign in ang admin. Huwag isama ang identifiers at credentials sa chat.',
        'ai-system-rules.md'),
    'offline': ('Local services and hardware limits',
        'Normal dashboard and queue functions do not depend on Ollama. Event analysis needs the local model and database; simple social replies remain available while the model loads. If a service is unavailable, I will say so. Physical ESP32 integration is still pending, so simulator data must stay labelled separately.',
        'Hindi nakadepende sa Ollama ang normal dashboard at pila. Kailangan ng local model at database ang event analysis; pwede pa rin ang simpleng usapan habang naglo-load ang model. Sasabihin ko kung unavailable ang service. Pending pa ang physical ESP32 integration, kaya hiwalay at labelled ang simulator data.',
        'admin-assistant.md'),
    'results': ('Results and leaderboard',
        'The backend validates completed round evidence before using a result in analytics or rankings. Win, zero-overlap loss and timeout are different outcomes. The leaderboard uses each player’s best valid result in the selected cohort. Missing denominators mean N/A; simulator and device results must not be mixed silently.',
        'Backend ang nagva-validate ng completed-round evidence bago gamitin ang result sa analytics o rankings. Magkakaiba ang panalo, zero-overlap loss at timeout. Best valid result ng bawat player sa selected cohort ang gamit ng leaderboard. N/A kapag walang denominator; hindi basta pinagsasama ang simulator at device results.',
        'admin-assistant.md'),
    'assistant': ('What Stack Intelligence can do',
        'I’m Stack Intelligence, your Stack Moko Baby assistant. You can discuss how this system works, ask follow-up questions or check saved event metrics in English or Taglish. My answers use reviewed system context and validated analytics. I cannot browse unrelated subjects, change game data or treat conversation claims as verified system facts.',
        'Ako si Stack Intelligence, ang assistant mo sa Stack Moko Baby. Pwede nating pag-usapan kung paano gumagana ang system, mag-follow-up o tumingin ng saved event metrics sa English o Taglish. Reviewed system context at validated analytics ang basehan ko. Hindi ako nagba-browse ng ibang paksa, nagbabago ng game data o tumuturing sa usapan bilang verified system fact.',
        'ai-system-rules.md'),
    'memory': ('Conversation memory',
        'I can remember validated topics, filters and your language or answer-length preference privately for your admin account. I do not save raw messages, private identifiers or old scores as current facts. Use the memory controls to switch this off or forget saved memory. Approved corrections from past chats can also guide future question interpretation when memory is enabled. This improves continuity and routing; it does not automatically retrain Ollama’s model weights.',
        'Pwede kong matandaan ang validated topics, filters at language o haba ng sagot na gusto mo, private sa admin account mo. Hindi ako nagsa-save ng raw messages, private identifiers o lumang scores bilang current facts. Pwede mong i-off o i-forget ang saved memory. Nakakatulong din ang approved corrections sa pag-intindi ng susunod na tanong kapag enabled ang memory. Para ito sa continuity at routing; hindi nito awtomatikong nire-retrain ang model weights ng Ollama.',
        'admin-assistant.md'),
}

# Related reviewed cards give a request for more detail additional sourced content.
RELATED_KNOWLEDGE = {
    'registration':'queue_flow', 'queue_flow':'registration', 'architecture':'offline',
    'gameplay':'results', 'results':'gameplay', 'offline':'architecture', 'privacy':'registration',
    'memory':'privacy', 'training':'memory', 'assistant':'dashboard', 'dashboard':'assistant',
}


SOCIAL_QUESTIONS = {
    'greeting': 'hello', 'thanks': 'thank you', 'identity': 'who are you', 'help': 'what can you do',
    'acknowledge': 'okay', 'farewell': 'goodbye', 'wellbeing': 'how are you',
}
