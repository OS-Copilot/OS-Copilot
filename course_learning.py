from oscopilot import FridayAgent, FridayExecutor, FridayPlanner, FridayRetriever, SelfLearner, SelfLearning, ToolManager, TextExtractor
from oscopilot.utils import setup_config


args = setup_config()
software_name = args.software_name
package_name = args.package_name
demo_file_path = args.demo_file_path

friday_agent = FridayAgent(FridayPlanner, FridayRetriever, FridayExecutor, ToolManager, config=args)
self_learning = SelfLearning(friday_agent, SelfLearner, ToolManager, args, TextExtractor)

# Only one stage of course study
# self_learning.self_learning(software_name, package_name, demo_file_path)

# contiunous learning
self_learning.continuous_learning(software_name, package_name, demo_file_path)