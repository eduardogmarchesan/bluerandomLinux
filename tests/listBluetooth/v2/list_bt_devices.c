#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/list.h>
#include <linux/rculist.h>
#include <net/bluetooth/bluetooth.h>
#include <net/bluetooth/hci_core.h>

// Verifique se hci_dev_list é visível: deve estar declarada em hci_core.h ou acessível externamente.
// Normalmente, a lista e o lock são internos ao hci_core.c. 
// Se não estiver exportada, você precisará modificar o kernel ou incluir o código dentro do kernel.
extern struct list_head hci_dev_list;

static int __init list_hci_devices_init(void)
{
    struct hci_dev *hdev;

    printk(KERN_INFO "Kernel Bluetooth Device Lister: Iniciando...\n");

    // A lista hci_dev_list é protegida por RCU, então precisamos do lock de leitura RCU
    rcu_read_lock();
    list_for_each_entry_rcu(hdev, &hci_dev_list, list) {
        // hdev->name: nome da interface hci (ex: "hci0")
        // hdev->bdaddr: endereço bluetooth do dispositivo
        // Para imprimir o endereço MAC do dispositivo de forma amigável, usamos o %pMR:
        // %pMR formata um endereço MAC reverso (como o usado em Bluetooth)
        printk(KERN_INFO "Encontrado dispositivo: %s, Endereço: %pMR\n", hdev->name, &hdev->bdaddr);
    }
    rcu_read_unlock();

    return 0;
}

static void __exit list_hci_devices_exit(void)
{
    printk(KERN_INFO "Kernel Bluetooth Device Lister: Encerrando...\n");
}

module_init(list_hci_devices_init);
module_exit(list_hci_devices_exit);

