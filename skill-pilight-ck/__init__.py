# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from pilight import pilight

# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.  You extend this class as shown below.

# TODO: Change "Template" to a unique name for your skill
class PilightCKSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(PilightCKSkill, self).__init__(name="PilightCKSkill")

        # Initialize working variables used within the skill.
        self.data = {"protocol": [ "intertechno_old" ], "id": 1, "unit": 0, "off": 1 }
        pilight_client = pilight.Client(host='pick', port=5000)

    # The "handle_xxxx_intent" function is triggered by Mycroft when the
    # skill's intent is matched.  The intent is defined by the IntentBuilder()
    # pieces, and is triggered when the user's utterance matches the pattern
    # defined by the keywords.  In this case, the match occurs when one word
    # is found from each of the files:
    #    vocab/en-us/Hello.voc
    #    vocab/en-us/World.voc
    # In this example that means it would match on utterances like:
    #   'Hello world'
    #   'Howdy you great big world'
    #   'Greetings planet earth'
    @intent_handler(IntentBuilder("").require("Hello").require("World"))
    def handle_hello_world_intent(self, message):
        # In this case, respond by simply speaking a canned response.
        # Mycroft will randomly speak one of the lines from the file
        #    dialogs/en-us/hello.world.dialog
        self.speak_dialog("hello.world")

    @intent_handler(IntentBuilder("LightOn").require("Light").require("State"))
    def handle_count_intent(self, message):
        if message.data["State"] == "on":
            self.data = {"protocol": [ "intertechno_old" ], "id": 1, "unit": 0, "on": 1 }
            self.speak_dialog("light.is.now.on")
        else:  # assume "off"
            self.data = {"protocol": [ "intertechno_old" ], "id": 1, "unit": 0, "off": 1 }
            self.speak_dialog("light.is.now.off")
        pilight_client.send_code(self.data)

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    # def stop(self):
    #    return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return PilightCKSkill()
