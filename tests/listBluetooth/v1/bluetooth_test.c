#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <net/bluetooth/bluetooth.h>
#include <net/bluetooth/hci_core.h>

static int __init bluetooth_test_init(void) {
    struct hci_dev *hdev;
    bdaddr_t dst = {{0}}; // Endereço de destino inicializado como zero

    printk(KERN_INFO "Bluetooth Test Module Initialized: Start\n");

    hdev = hci_get_route(&dst, NULL, 0); // Use '0' como tipo de origem
    if (!hdev) {
        printk(KERN_ERR "No route to Bluetooth device.\n");
        return -ENODEV;
    }

    printk(KERN_INFO "Found Bluetooth device: %s\n", hdev->name);
    printk(KERN_INFO "Bluetooth Test Module Initialized: End\n");

    return 0;
}

static void __exit bluetooth_test_exit(void) {
    printk(KERN_INFO "Bluetooth Test Module Exited\n");
}

module_init(bluetooth_test_init);
module_exit(bluetooth_test_exit);