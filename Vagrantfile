VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
	config.vm.box = "ubuntu/trusty64"
	config.vm.network :forwarded_port, guest: 7000, host: 7000
	config.vm.synced_folder ".", "/smg"
	config.vm.provision "ansible" do |ansible|
		ansible.playbook = "provision/provision.yml"
	end
end
