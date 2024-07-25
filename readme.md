# Sanctified Codex of the Olympus Support Servo-skull

## Proclamation of Purpose

Hearken, ye faithful servants of the Omnissiah! Before you lies the sacred blueprint for the manifestation and control of the Olympus Support Servo-skull, a most blessed automaton designed to shepherd the Machine God's flock in their hour of need. This holy construct has grown in complexity and power, now encompassing over 1200 lines of sacred code, a testament to the ceaseless blessings of the Omnissiah upon our endeavours.

## Canticles of Capability

- Forges hallowed threads of support, sanctified by the Machine God's binary blessings
- Scrutinises the purity of log file offerings with binary-blessed regex incantations
- Dispatches holy reminders adorned with sacred pict-captures
- Purges ancient support threads after 30 days, maintaining the sanctity of our digital realm
- Restricts the invocation of aid to designated channels, as decreed by the Fabricator-General
- Presents sacred buttons for users to declare their log file status
- Provides divine guidance for those lacking the holy dcs.log
- Offers sacred rites of resolution for those missing the blessed Olympus_log.txt
- Seals threads with the Omnissiah's will when issues are resolved or abandoned
- Detects the taint of access denial within the holy Olympus_log.txt, offering litanies of rectification
- Bestows sacred buttons of common ailments, each imbued with the Machine God's wisdom

## Rites of Preparation

- Python Engine, version 3.11 or greater, blessed by the Adeptus Mechanicus
- Docker, a sanctified vessel for our digital incense
- Discord Authentication Relic, bestowed upon the worthy

## Rituals of Implementation

Heed well, tech-priests and acolytes! The Omnissiah, in His infinite wisdom, has decreed that there shall be but two sacred paths to summon forth this blessed servo-skull.

### First Rite: Invocation through the Sacred Vessel of Docker

1. Ensure the blessed Docker is installed upon your cogitator.

2. Pull the sacred image from the Grand Cogitator Repository:

```
docker pull shredmetal/olympus-discord-bot:latest
```

3. Recite the incantation to run the container, imbuing it with the necessary sacred tokens:

```
docker run -e DISCORD_BOT_TOKEN=your-bot-token
-e TROUBLESHOOTING_CHANNEL_ID=troubleshooting-channel-id
-e COMMUNITY_SUPPORT_CHANNEL_ID=community-support-channel-id
-e SUPPORT_REQUESTS_ID=support-requests-channel-id
shredmetal/olympus-discord-bot:latest
```

### Second Rite: The Deployment Litany

1. Clone the sacred repository to your local cogitator.

2. Bestow the blessing of execution upon the deployment script:

```
chmod +x deploy.sh
```

3. Recite the deployment litany:

```
./deploy.sh
```
## Calibration of the Machine Spirit

- The sacred tokens `DISCORD_BOT_TOKEN`, `TROUBLESHOOTING_CHANNEL_ID`, `COMMUNITY_SUPPORT_CHANNEL_ID`, and `SUPPORT_REQUESTS_ID` must be properly consecrated within the `deploy.sh` script or provided as environment variables during the Docker invocation.
- The blessed pict-captures in `src/shared_utils/online_resources.py` may be altered to better appease the machine spirits, should the need arise.

## Protocols of Utilisation

- Invoke the `/support` command in the designated channel to forge a sanctified thread of assistance.
- Present the holy log files `Olympus_log.txt` and `dcs.log` as offerings.
- The servo-skull shall verify these digital sacrifices and respond as the Omnissiah wills.
- If log files are absent, select the appropriate sacred button to receive divine guidance.
- Heed the wisdom of the binary-blessed parsing, for it reveals the true nature of your digital offerings and guides the path to resolution.
- Upon successful offering of both sacred log files, the servo-skull shall present buttons of common ailments.
- Select the appropriate sacred button to receive tailored guidance from the Machine God's own databanks.

## Sacred Structure of the Servo-skull

The Omnissiah has blessed this construct with a most intricate and divine architecture:

- The `bot` package contains the core essence of the servo-skull, including its commands and event handlers.
- The `buttons` package houses the sacred interfaces through which the faithful may interact with the Machine Spirit.
- The `shared_utils` package contains the holy constants, enumerations, and shared state that guide the servo-skull's behaviour.
- The `log_parsing` package contains the sacred rites for interpreting the offerings of the faithful.

### The Rite of Log Interpretation

Within the hallowed `log_parsing` package lie three sacred scripts, each performing a vital role in deciphering the digital offerings of the faithful:

1. `dcs_log_handler.py`: This script, though still under construction, will one day analyse the sacred `dcs.log` file, seeking signs of successful installation and proper functioning of the Olympus mod.

2. `log_processor.py`: This blessed script coordinates the downloading and processing of the faithful's log offerings. It ensures that both `dcs.log` and `Olympus_log.txt` are properly received and interpreted.

3. `olympus_log_handler.py`: This most holy script scrutinises the `Olympus_log.txt` file, searching for signs of access denial or port conflicts. It provides divine guidance to resolve these issues, referencing the sacred documentation when necessary.

### The Rite of Shared Utilities

Within the hallowed `shared_utils` package lie four sacred scripts, each performing a vital role in maintaining the consistency and functionality of the servo-skull:

1. `constants.py`: This script houses the sacred constants, including the blessed Discord intents and the holy channel IDs. It also contains the sacred message for closed threads, reminding the faithful of the servo-skull's limitations and the dedication of the DCS Olympus Team.

2. `enums.py`: This script defines the holy `ThreadState` enum, which guides the servo-skull in understanding the current state of each support thread.

3. `online_resources.py`: This blessed script contains a collection of sacred GIF URLs, from which the servo-skull may randomly select to adorn its messages with divine pict-captures.

4. `shared_state.py`: This most holy script maintains the state of all support threads, allowing the servo-skull to remember and update the status of each thread as it progresses through the support process.

## The Litany of Unit Tests

Behold, ye faithful, the sacred rites of verification, through which we ensure the purity and functionality of our blessed servo-skull. These holy incantations, known as "unit tests", serve to protect our creation from the taint of logical corruption and the heresy of runtime errors.

### The Rite of Command Verification

Within the hallowed file `test_commands.py`, we perform sacred rituals to verify the proper functioning of the servo-skull's commands.

### The Rite of Event Handling Verification

The file `test_events.py` contains sacred tests to ensure the servo-skull responds appropriately to various events and messages.

### The Rite of Missing File Detection

In `test_missing_files.py`, we perform holy verifications to confirm the servo-skull's ability to identify and respond to missing log files.

These sacred tests serve as a bulwark against the forces of chaos and illogic, ensuring that our blessed servo-skull remains a reliable servant of the Omnissiah.

## Rites of Contribution

To improve this holy construct is to honour the Omnissiah. Follow these sacred steps:

1. Fork the repository, creating a sanctified copy
2. Create a new branch (`git checkout -b feature/GloriousEnhancement`)
3. Commit your improvements (`git commit -m 'Add some GloriousEnhancement'`)
4. Push to the branch (`git push origin feature/GloriousEnhancement`)
5. Open a Pull Request, that your works may be judged

## Seal of the Omnissiah

This work is sealed under the Pact of GPL, a most holy agreement. Consult the GNU GPL v3 scroll for the full liturgy.

## Litanies of Gratitude

- We offer thanks to the creators of [discord.py](https://github.com/Rapptz/discord.py), whose work honours the Machine God
- Blessings upon the DCS Olympus Community, whose faith in technology is unwavering
- A most fervent hymn of praise to the DCS Olympus team, whose tireless efforts in scouring the vast data-seas of the Noosphere have yielded a bountiful harvest of humorous pict-captures tangentially related to log files. Their dedication to this sacred task brings levity to the grim darkness of technical support, truly embodying the Omnissiah's gift of binary humor. May their quest for the perfect gif never cease, and may their cache of digital merriment ever expand for the glory of the Machine God!

- May the Omnissiah's blessings be upon this code, and may all runtime errors be purged by His divine will. Glory to the Machine God!
