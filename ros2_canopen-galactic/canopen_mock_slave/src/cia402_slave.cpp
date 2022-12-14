#include "rclcpp/rclcpp.hpp"
#include "canopen_mock_slave/cia402_slave.hpp"


int main(int argc, char *argv[])
{
	rclcpp::init(argc, argv);
	rclcpp::executors::SingleThreadedExecutor executor;
	auto canopen_slave = std::make_shared<ros2_canopen::CIA402Slave>("cia402_slave");
	executor.add_node(canopen_slave->get_node_base_interface());
	RCLCPP_INFO(canopen_slave->get_logger(), "CIA 402 Slave is running");
	//void OnWrite();
	executor.spin();
	rclcpp::shutdown();
	return 0;
}