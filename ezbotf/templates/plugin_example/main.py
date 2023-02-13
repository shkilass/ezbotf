
import ezbotf

plugin = ezbotf.Plugin(ezbotf.PluginType.Standalone)


@plugin.on_load
def on_load():
    @plugin.command(plugin.translator.translations['command']['hello']['names'])
    async def hello(event, _):
        await ezbotf.messages.info(event, plugin.runtime_config['text'])
