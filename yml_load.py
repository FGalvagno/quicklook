import yaml 
import glob
from datetime import datetime as dt, timedelta as tdelta
class lidarConfig:
    def __init__(self, config_folder):
        #config_dict.update({f.name[9:-4]: yaml.safe_load(f)})
        
        file_prefix = dict(
            COR= 'h',
            TUC= 't',
            VM = 'a',
            SMN= 'a',
            NQN= 'n',
            BAR= 'b',
            COM= 'c',
            OAPA= 'r'
        )
        
        try:
            with open(config_folder+'/config_global.yml', 'r') as f:
                self.global_config = yaml.safe_load(f)
            with open(config_folder+'/config_'+self.global_config['site']+'.yml', 'r') as f:
                self.local_config = yaml.safe_load(f)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            print("Please check the configuration files.")
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            print("Please check the configuration files.")
        
        self.location_prefix = file_prefix[self.global_config['site']]

        """
        Initialize the lidar_config class with a dictionary of configuration settings.
        
        Args:
            config_dict (dict): Dictionary containing configuration settings.
        """

    def get_src(self):
        return self.local_config['src']
    
    def get_dateinterval(self):
        if(self.global_config['plot_last_days']):
            datearray = [dt.now()-tdelta(days=self.global_config['days_to_plot']), dt.now()]
        else:
            datearray = [dt.strptime(self.global_config['starting_date'], "%Y-%m-%d"), dt.strptime(self.global_config['end_date'], "%Y-%m-%d")]
        return datearray

    def get_channel(self):
        return self.local_config['channel']
    

