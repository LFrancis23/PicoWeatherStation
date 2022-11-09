#include <stdio.h>

#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
#include "boards/pico_w.h"

char ssid[] = "Telephone Line";
char pass[] = "ElectricLightsOrchestra";

int main(){
        stdio_init_all();
        if (cyw43_arch_init_with_country(CYW43_COUNTRY_USA)) {
                printf("Failed to initialize\n");
                return 1;
        }
        printf("Initialized\n");

        cyw43_arch_enable_sta_mode();

        if (cyw43_arch_wifi_connect_timeout_ms(ssid,pass,CYW43_AUTH_WPA2_AES_PSK, 10000)) {
                printf("Failed to connect\n");
                return 1;
        }
        printf("Connected\n"); 
        while(1){
                printf("Testing\n");
                cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN,1);
                sleep_ms(1000);
                cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN,0);
        }
}